import functools
import os
import ssl
from datetime import date, time
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Case, When, F, Q, Count, Value, FloatField, ExpressionWrapper,IntegerField
from django.db.models.functions import Coalesce
from django.db import connection, connections
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView
from django.http import HttpResponse
from docxtpl import DocxTemplate
from number_to_string import get_string_by_number
from openpyxl import Workbook
from docx import Document
from ktscrm import settings
from .models import *


class GuardedObjectDetailView(DetailView):
    model = GuardedObjects
    template_name = 'guarded_objects.html'
    context_object_name = 'guarded_object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guarded_object = self.get_object()

        # Fetch related alarms and schedules
        request = Alarms.objects.filter(objectid=guarded_object, clazz='Request')
        alarms = Alarms.objects.filter(objectid=guarded_object, clazz='Alarm')
        alarm_schedules = AlarmSchedules.objects.filter(
            models.Q(id=guarded_object.alarmscheduleid.id) |
            models.Q(id=guarded_object.firescheduleid.id) |
            models.Q(id=guarded_object.securityscheduleid.id)
        )
        guarded_zone = GuardedZones.objects.filter(objectid=guarded_object)

        context['alarms'] = alarms
        context['request'] = request
        context['guarded_zone'] = guarded_zone
        context['alarm_schedules'] = alarm_schedules
        return context


class EkcBaza(ListView):
    model = GuardedObjects
    template_name = 'baza_ekc.html'
    context_object_name = 'klienty'

    def get(self, request, *args, **kwargs):
        queryset = GuardedObjects.objects.all()
        query = self.request.GET.get('q')
        number = self.request.GET.get('number')
        company_id = self.request.GET.get('company_id')
        crew = self.request.GET.get('crew')

        if query:
            queryset = queryset.filter(
                Q(number__icontains=query) |
                Q(name__icontains=query) |
                Q(address__icontains=query)
            )
        if number:
            queryset = queryset.filter(number__icontains=number)
        if company_id:
            queryset = queryset.filter(companyid__exact=company_id)
        if crew:
            queryset = queryset.filter(crew__icontains=crew)

        # Add ordering to the queryset
        queryset = queryset.order_by('id')

        paginator = Paginator(queryset, per_page=25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        params = request.GET.copy()
        if 'page' in params:
            del params['page']
        pagination_url = request.path + '?' + urlencode(params)

        # Получение уникальных компаний для фильтра
        unique_companies = Users.objects.filter(
            id__in=GuardedObjects.objects.values('companyid')
        ).distinct()

        # Получение уникальных групп реагирования для фильтра
        unique_crews = GuardedObjects.objects.values_list('crew', flat=True).distinct()

        return render(request, self.template_name, {
            'klienty': page_obj,
            'pagination_url': pagination_url,
            'total_entries': queryset.count(),
            'unique_companies': unique_companies,
            'unique_crews': unique_crews,
        })


def reports_technician(request):
    report_data = GuardedObjects.objects.values('technician').annotate(
        total_records=Count('technician'),
        legalentity_true_count=Count('technician', filter=Q(legalentity=True)),
        legalentity_false_count=Count('technician', filter=Q(legalentity=False))
    ).order_by('-total_records')

    context = {
        'report_data': report_data
    }

    return render(request, 'reports_technician.html', context)


def reports_crew(request):
    # Фильтруем объекты по companyid и группируем по crew
    crew_stats = GuardedObjects.objects.filter(companyid=5).values('crew').annotate(
        total_count=Count('crew'),
        legal_count=Count('id', filter=Q(legalentity=True)),
        physical_count=Count('id', filter=Q(legalentity=False))
    )

    # Разделяем crew на те, что от 1 до 22 и остальные
    sorted_crew_stats = sorted(crew_stats, key=lambda x: (int(x['crew']) if x['crew'].isdigit() and 1 <= int(x['crew']) <= 22 else float('inf'), x['crew']))

    return render(request, 'reports_crew.html', {'crew_stats': sorted_crew_stats})


def reports_crew(request):
    with connections['asu_ekc'].cursor() as cursor:
        cursor.execute("""
WITH duration_sums AS (
    SELECT 
        go.crew,
        go.legalentity,
        COALESCE(a1.duration, 0) AS alarmschedule_duration,
        COALESCE(a2.duration, 0) AS fireschedule_duration,
        COALESCE(a3.duration, 0) AS securityschedule_duration,
        CASE
            WHEN COALESCE(a1.duration, 0) = COALESCE(a2.duration, 0) AND COALESCE(a2.duration, 0) = COALESCE(a3.duration, 0) THEN LEAST(730, COALESCE(a1.duration, 0) + COALESCE(a2.duration, 0))
            WHEN COALESCE(a2.duration, 0) = COALESCE(a3.duration, 0) THEN LEAST(730, COALESCE(a1.duration, 0) + COALESCE(a3.duration, 0))
            WHEN COALESCE(a1.duration, 0) = COALESCE(a3.duration, 0) THEN LEAST(730, COALESCE(a1.duration, 0) + COALESCE(a2.duration, 0))
            ELSE LEAST(730, COALESCE(a1.duration, 0) + COALESCE(a2.duration, 0) + COALESCE(a3.duration, 0))
        END AS total_duration
    FROM 
        guarded_objects go
    LEFT JOIN 
        alarm_schedules a1 ON go.alarmscheduleid = a1.id
    LEFT JOIN 
        alarm_schedules a2 ON go.firescheduleid = a2.id
    LEFT JOIN 
        alarm_schedules a3 ON go.securityscheduleid = a3.id
    WHERE
        go.companyid = 5
)
SELECT 
    crew,
    COUNT(*) AS total_count,
    SUM(CASE WHEN legalentity = TRUE THEN 1 ELSE 0 END) AS legal_count,
    SUM(CASE WHEN legalentity = FALSE THEN 1 ELSE 0 END) AS physical_count,
    SUM(CASE WHEN legalentity = TRUE THEN total_duration ELSE 0 END) AS total_hours_legal,
    SUM(CASE WHEN legalentity = TRUE THEN total_duration ELSE 0 END) * 9 AS total_legal_sum,
    SUM(CASE WHEN legalentity = FALSE THEN 1 ELSE 0 END) * 1500 AS total_physical_sum,
    SUM(CASE WHEN legalentity = TRUE THEN total_duration ELSE 0 END) * 9 + SUM(CASE WHEN legalentity = FALSE THEN 1 ELSE 0 END) * 1500 AS total_sum
FROM 
    duration_sums
GROUP BY 
    crew
ORDER BY 
    crew;
        """)
        results = cursor.fetchall()

    crew_stats = []
    for row in results:
        crew_stats.append({
            'crew': row[0],
            'total_count': row[1],
            'legal_count': row[2],
            'physical_count': row[3],
            'total_hours_legal': row[4],
            'total_legal_sum': row[5],
            'total_physical_sum': row[6],
            'total_sum': row[7],
        })

    return render(request, 'reports_crew.html', {'crew_stats': crew_stats})



def export_crew_to_excel(request):
    # Создание книги Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Отчет по Экипажам"

    # Заголовки столбцов
    columns = [
        "ID", "Номер объекта", "Тип", "Компания", "Экипаж", "Юрлицо",
        "Охранная сигнализация", "Тревожная сигнализация",
        "Пожарная сигнализация", "Итог часов"
    ]
    ws.append(columns)

    # Получение данных из базы данных
    crew_data = GuardedObjects.objects.filter(companyid=5).prefetch_related(
        'alarmscheduleid', 'firescheduleid', 'securityscheduleid', 'companyid'
    )
    total_records = crew_data.aggregate(total=Count('id'))['total']
    print(f"Total records: {total_records}")

    for obj in crew_data:
        alarmschedule_duration = obj.alarmscheduleid.duration if obj.alarmscheduleid else 0
        fireschedule_duration = obj.firescheduleid.duration if obj.firescheduleid else 0
        securityschedule_duration = obj.securityscheduleid.duration if obj.securityscheduleid else 0

        total_duration = alarmschedule_duration + fireschedule_duration + securityschedule_duration
        if alarmschedule_duration == fireschedule_duration == securityschedule_duration:
            total_duration = alarmschedule_duration + fireschedule_duration
        elif fireschedule_duration == securityschedule_duration:
            total_duration = alarmschedule_duration + securityschedule_duration
        elif alarmschedule_duration == securityschedule_duration:
            total_duration = alarmschedule_duration + fireschedule_duration
        total_duration = min(total_duration, 730)

        row = [
            obj.id,
            obj.literal+"-"+obj.number,
            obj.type,
            obj.companyid.username if obj.companyid else "",
            obj.crew,
            "Да" if obj.legalentity else "Нет",
            alarmschedule_duration,
            fireschedule_duration,
            securityschedule_duration,
            total_duration
        ]
        ws.append(row)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Подготовка ответа
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=crew_report.xlsx'

    return response


def group_days(schedule):
    days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    times = [
        (schedule.mondaystart or time(0, 0), schedule.mondayend or time(0, 0)),
        (schedule.tuesdaystart or time(0, 0), schedule.tuesdayend or time(0, 0)),
        (schedule.wednesdaystart or time(0, 0), schedule.wednesdayend or time(0, 0)),
        (schedule.thursdaystart or time(0, 0), schedule.thursdayend or time(0, 0)),
        (schedule.fridaystart or time(0, 0), schedule.fridayend or time(0, 0)),
        (schedule.saturdaystart or time(0, 0), schedule.saturdayend or time(0, 0)),
        (schedule.sundaystart or time(0, 0), schedule.sundayend or time(0, 0))
    ]

    groups = []
    current_group = [days[0]]
    current_time = times[0]

    for i, day_time in enumerate(times[1:], start=1):
        if day_time == current_time:
            current_group.append(days[i])
        else:
            groups.append((current_group, current_time))
            current_group = [days[i]]
            current_time = day_time

    groups.append((current_group, current_time))

    result = []
    for group, day_time in groups:
        if len(group) == 7:
            if day_time == (time(0, 0), time(0, 0)):
                result.append("ПН-ВС КРУГЛОСУТОЧНО")
            else:
                time_str = f"{day_time[0].strftime('%H:%M')}-{day_time[1].strftime('%H:%M')}"
                result.append(f"ПН-ВС {time_str}")
        else:
            if group == ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ']:
                days_str = "ПН-ПТ"
            elif group == ['СБ', 'ВС']:
                days_str = "СБ-ВС"
            else:
                days_str = "-".join(group) if len(group) > 1 else group[0]
            time_str = f"{day_time[0].strftime('%H:%M')}-{day_time[1].strftime('%H:%M')}" if day_time[0] and day_time[1] else "00:00-00:00"
            result.append(f"{days_str} {time_str}")

    return ", ".join(result)



def generate_word(request, object_id):
    if request.method == "GET":
        guarded_object = get_object_or_404(GuardedObjects, pk=object_id)

        alarm_schedules = AlarmSchedules.objects.filter(
            models.Q(id=guarded_object.alarmscheduleid_id) |
            models.Q(id=guarded_object.firescheduleid_id) |
            models.Q(id=guarded_object.securityscheduleid_id)
        )

        security_duration = 0
        fire_duration = 0
        alarm_duration = 0

        for schedule in alarm_schedules:
            if schedule.enabled:
                if schedule.dtype == 'SECURITY':
                    security_duration = schedule.duration if schedule.duration <= 730 else 730
                elif schedule.dtype == 'FIRE':
                    fire_duration = schedule.duration if schedule.duration <= 730 else 730
                elif schedule.dtype == 'ALARM':
                    alarm_duration = schedule.duration if schedule.duration <= 730 else 730

        if security_duration == fire_duration == alarm_duration:
            total_duration = security_duration
        elif security_duration == fire_duration:
            total_duration = security_duration + alarm_duration
        elif security_duration == alarm_duration:
            total_duration = security_duration + fire_duration
        else:
            total_duration = security_duration + fire_duration + alarm_duration

        total_duration = min(total_duration, 730)

        if guarded_object.legalentity:
            payment = total_duration * 9
        else:
            payment = 1500

        template_path = os.path.join(settings.MEDIA_ROOT, 'perechen.docx')
        doc = DocxTemplate(template_path)

        current_date = date.today().strftime("%d.%m.%Y")

        alarm_schedules_data = []
        for schedule in alarm_schedules:
            if schedule.enabled:
                grouped_days_str = group_days(schedule)
                alarm_schedules_data.append({
                    'type': 'Охранная сигнализация' if schedule.dtype == 'SECURITY' else 'Пожарная сигнализация' if schedule.dtype == 'FIRE' else 'Тревожная сигнализация',
                    'grouped_days_str': grouped_days_str,
                    'total': schedule.duration,
                })

        company_name = ''
        director_name = ''
        if guarded_object.crew in ('1','2','3','4','11','18','19'):
            company_name = 'Акинак Бодигард'
            director_name = 'Юрьев А.А.'
        elif guarded_object.crew in ('7','8','9','14','15','21'):
            company_name = 'Кузет 24/7'
            director_name = 'Айтказинов С.К.'
        else:
            company_name = 'Кузет-Сенiм'
            director_name = 'Иванова Л.В.'

        print(guarded_object.type)


        context = {
            'date': current_date,
            'object_name': guarded_object.name,
            'object_type': guarded_object.type,
            'object_number': guarded_object.literal +'-'+ guarded_object.number,
            'object_address': guarded_object.address,
            'time_pribitia': guarded_object.arrivingtime,
            'alarm_schedules': alarm_schedules_data,
            'total_duration': total_duration,
            'payment': payment,
            'company_name': company_name,
            'director_name': director_name,
        }

        doc.render(context)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename={guarded_object.literal}-{guarded_object.number}.docx'
        doc.save(response)
        return response

    return HttpResponse(status=405)  # Method not allowed


















