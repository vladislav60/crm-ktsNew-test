from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from urllib.parse import urlencode
# from django.contrib.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from docxtpl import DocxTemplate
import os
from datetime import *
from number_to_string import get_string_by_number
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import pandas as pd
from django.urls import reverse
from .forms import ExcelImportForm
from .models import *
import numpy as np
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.utils.dateparse import parse_date

from .forms import *
from .models import *

# from .utils import *

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def logout_view(request):
    logout(request)
    return redirect('login')


# №2 Шаблон главной страницы
@login_required
def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница'
    }
    return render(request, 'dogovornoy/index.html', context=context)


# Шаблон создание договоров
@login_required
def create_dogovor(request, klient_id):
    if request.method == "GET":
        passport_info = kts.objects.get(pk=klient_id)
        vid_sign1 = vid_sign.objects.get(pk=passport_info.vid_sign_id)
        if ((passport_info.mat_otv == '0') and (passport_info.urik == False)):
            doc = DocxTemplate(os.path.abspath('media/ots-fizlica-bezmat.docx'))
            split_names_klient_ = passport_info.klient_name.split()
            short_names_klient = f'{split_names_klient_[0]} {split_names_klient_[1][0]}.{split_names_klient_[2][0]}.'.title()
        elif ((passport_info.mat_otv == '0') and (passport_info.urik == True)):
            doc = DocxTemplate(os.path.abspath('media/ОС-ТС юр.лиц.нов без мат.ответственности.docx'))
            short_names_klient = ""
        elif ((passport_info.mat_otv != '0') and (passport_info.urik == False)):
            doc = DocxTemplate(os.path.abspath('media/Договор ОТС Квартира-дом физ.лицо.docx'))
            split_names_klient_ = passport_info.klient_name.split()
            short_names_klient = f'{split_names_klient_[0]} {split_names_klient_[1][0]}.{split_names_klient_[2][0]}.'.title()
        elif (passport_info.urik == False) and (vid_sign1.name_sign == 'тс'):
            doc = DocxTemplate(os.path.abspath('media/ТС физ.лица без материальной.docx'))
            split_names_klient_ = passport_info.klient_name.split()
            short_names_klient = f'{split_names_klient_[0]} {split_names_klient_[1][0]}.{split_names_klient_[2][0]}.'.title()
        elif (passport_info.urik == True) and (vid_sign1.name_sign == 'тс'):
            doc = DocxTemplate(os.path.abspath('media/ТС юр.лица без материальной.docx'))
            short_names_klient = ""
        elif (passport_info.mat_otv != '0') and (passport_info.urik == True) and (
                (vid_sign1.name_sign == 'ОТС') or (vid_sign1.name_sign == 'ОС')):
            doc = DocxTemplate(os.path.abspath('media/ОС-ТС юр.лиц. нов для ИП.docx'))
            short_names_klient = ""
        else:
            print('test')

        rekvizity_test = rekvizity.objects.get(pk=passport_info.company_name_id)
        current_date = date.today()
        current_date = current_date.strftime("%d/%m/%Y")
        currency_main = ('тенге', 'тенге', 'тенге')
        currency_additional = ('тиын', 'тиына', 'тиынов')
        itog_oplata_propis = get_string_by_number(passport_info.itog_oplata, currency_main, currency_additional)
        time_reag_propis = get_string_by_number(passport_info.time_reag, currency_main, currency_additional)
        oplata_itog1 = itog_oplata_propis.split(' тенге 00 тиынов')
        time_reag_itog1 = time_reag_propis.split(' тенге 00 тиынов')
        time_reag_nebol_propis = get_string_by_number(passport_info.time_reag_nebol, currency_main, currency_additional)
        time_reag_nebol_itog1 = time_reag_nebol_propis.split(' тенге 00 тиынов')
        mat_otv_propis = get_string_by_number(passport_info.mat_otv, currency_main, currency_additional)
        mat_otv_itog1 = mat_otv_propis.split(' тенге 00 тиынов')
        mat_otv_itog2 = mat_otv_itog1[0].strip()

        if passport_info.email:
            email_itog = passport_info.email
        else:
            email_itog = ' '
        context = {
            'snames_klient': short_names_klient,
            'udv_number': passport_info.udv_number,
            'date_udv': passport_info.date_udv,
            'dogovor_number': passport_info.dogovor_number,
            'date': current_date,
            'date_zakl': passport_info.data_zakluchenia,
            'klient_name': passport_info.klient_name,
            'company_name': passport_info.company_name,
            'time_reag': passport_info.time_reag,
            'time_reag_itog1': time_reag_itog1[0],
            'time_reag_nebol': passport_info.time_reag_nebol,
            'time_reag_nebol_itog1': time_reag_nebol_itog1[0],
            'adres': passport_info.adres,
            'iin_bin': passport_info.iin_bin,
            'telephone': passport_info.telephone,
            'vid_sign_polnoe': vid_sign1.name_sign_polnoe,
            'vid_sign_sokr': vid_sign1.name_sign,
            'urik': passport_info.urik,
            'email': email_itog,
            'name_object': passport_info.name_object,
            'stoimost_rpo': passport_info.stoimost_rpo,
            'mat_otv': passport_info.mat_otv,
            'mat_otv_itog1': mat_otv_itog2,
            'itog_oplata': passport_info.itog_oplata,
            'itog_oplata_propis': oplata_itog1[0],
            'chasi_po_dog': passport_info.chasi_po_dog,
            'vid_rpo': passport_info.vid_rpo,
            'polnoe_name': rekvizity_test.polnoe_name,
            'adres_company': rekvizity_test.adres_company,
            'bin': rekvizity_test.bin,
            'iban': rekvizity_test.iban,
            'bic': rekvizity_test.bic,
            'bank': rekvizity_test.bank,
            'telephone_ofiice': rekvizity_test.telephone_ofiice,
            'telephone_buh': rekvizity_test.telephone_buh,
            'vid_too': rekvizity_test.vid_too,
            'doljnost': rekvizity_test.doljnost,
            'ucheriditel_name_polnoe': rekvizity_test.ucheriditel_name_polnoe,
            'ucheriditel_name_sokr': rekvizity_test.ucheriditel_name_sokr,
        }
        doc.render(context)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=download.docx'
        doc.save(response)

    return response


@method_decorator(login_required, name='dispatch')
class AddClient(FormView):
    template_name = 'dogovornoy/add_client.html'
    form_class = AddKlientDogForm
    success_url = '/baza_dogovorov/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, menu=menu, title='Новый клиент'))



@login_required
def update_client(request, klient_id):
    kartochka = get_object_or_404(kts, pk=klient_id)
    if request.method == 'POST':
        form = AddKlientDogForm(request.POST, request.FILES, instance=kartochka)
        if form.is_valid():
            form.save()
            return redirect('baza_dogovorov')
    else:
        form = AddKlientDogForm(instance=kartochka)
    return render(request, 'dogovornoy/update_client.html', {'form': form, 'kartochka': kartochka})


@login_required
def delete_client(request, klient_id):
    kartochka = get_object_or_404(kts, pk=klient_id)
    if request.method == 'POST':
        kartochka.delete()
        return redirect('baza_dogovorov')
    return render(request, 'dogovornoy/delete_client.html', {'kartochka': kartochka})


@method_decorator(login_required, name='dispatch')
class DogBaza(ListView):
    model = kts
    template_name = 'dogovornoy/baza_dogovorov.html'
    context_object_name = 'klienty'

    def get(self, request, *args, **kwargs):
        queryset = kts.objects.all()
        query = self.request.GET.get('q')
        company_names = rekvizity.objects.values_list('id', 'polnoe_name')
        object_number = self.request.GET.get('object_number')
        company_name = self.request.GET.get('company_name')
        dogovor_number = self.request.GET.get('dogovor_number')
        gruppa_reagirovania = self.request.GET.get('gruppa_reagirovania')

        if query:
            queryset = queryset.filter(
                Q(object_number__icontains=query) |
                Q(dogovor_number__icontains=query) |
                Q(klient_name__icontains=query) |
                Q(adres__icontains=query) |
                Q(telephone__icontains=query) |
                Q(iin_bin__icontains=query) |
                Q(name_object__icontains=query)
            )
        if object_number:
            queryset = queryset.filter(object_number__icontains=object_number)
        if company_name:
            queryset = queryset.filter(company_name_id__exact=company_name)
        if dogovor_number:
            queryset = queryset.filter(dogovor_number__icontains=dogovor_number)
        if gruppa_reagirovania:
            queryset = queryset.filter(gruppa_reagirovania__icontains=gruppa_reagirovania)

        paginator = Paginator(queryset, per_page=25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        params = request.GET.copy()
        if 'page' in params:
            del params['page']
        pagination_url = request.path + '?' + urlencode(params)

        return render(request, self.template_name, {'klienty': page_obj, 'company_names': company_names, 'pagination_url': pagination_url, 'total_entries': queryset.count()})



@method_decorator(login_required, name='dispatch')
class Rekvizity(ListView):
    model = rekvizity
    template_name = 'dogovornoy/rekvizity.html'
    context_object_name = 'rekvizity'


@login_required
def importexcel(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['excel_file']

            # Load the Excel data into a Pandas dataframe
            df = pd.read_excel(excel_file)
            df = df.replace({np.nan: None})
            print(df)
            # Iterate over the rows of the dataframe and create kts objects
            for index, row in df.iterrows():
                kts_obj = kts(
                    udv_number=row['udv_number'],
                    date_udv=row['date_udv'],
                    dogovor_number=row['dogovor_number'],
                    data_zakluchenia=row['data_zakluchenia'],
                    nalichiye_dogovora=row['nalichiye_dogovora'],
                    mat_otv=row['mat_otv'],
                    act_ty=row['act_ty'],
                    time_reag=row['time_reag'],
                    time_reag_nebol=row['time_reag_nebol'],
                    yslovie_dogovora=row['yslovie_dogovora'],
                    klient_name=row['klient_name'],
                    name_object=row['name_object'],
                    adres=row['adres'],
                    iin_bin=row['iin_bin'],
                    telephone=row['telephone'],
                    urik=row['urik'],
                    chasi_po_dog=row['chasi_po_dog'],
                    dop_uslugi=row['dop_uslugi'],
                    abon_plata=row['abon_plata'],
                    itog_oplata=row['itog_oplata'],
                    object_number=row['object_number'],
                    peredatchik_number=row['peredatchik_number'],
                    stoimost_rpo=row['stoimost_rpo'],
                    date_podkluchenia=row['date_podkluchenia'],
                    date_otklulchenia=row['date_otklulchenia'],
                    gruppa_reagirovania=row['gruppa_reagirovania'],
                    email=row['email'],
                    vid_rpo=row['vid_rpo'],
                    primechanie=row['primechanie'],
                    agentskie=row['agentskie'],
                    photo=row['photo'],
                    prochee=row['prochee'],
                    company_name_id=row['company_name_id'],
                    vid_sign_id=row['vid_sign_id']
                )
                kts_obj.save()

            # Redirect to the kts list page
            return HttpResponseRedirect(reverse('baza_dogovorov'))
    else:
        form = ExcelImportForm()

    return render(request, 'dogovornoy/importexel.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class KartochkaKlienta(DetailView):
    model = kts
    template_name = 'dogovornoy/kartochka_klienta.html'
    pk_url_kwarg = 'klient_id'
    context_object_name = 'kartochka'


# Страница 404
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сраница не найдена</h1>')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Страница отчеты договорной
@login_required
def reports(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month-1, 1, tzinfo=timezone.utc)
    end_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    companies = rekvizity.objects.all()
    urik_companies = rekvizity.objects.filter(kts__urik=True, kts__date_otklulchenia=None)
    non_urik_companies_quantity = rekvizity.objects.filter(kts__urik=False, kts__date_otklulchenia=None)

    reports = []

    for company in companies:
        # 1 otlk
        kts_otkl = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                      date_otklulchenia__lt=end_of_month)
        kts_abon_summa = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lt=end_of_month).aggregate(Sum('abon_plata'))
        kts_count = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                       date_otklulchenia__lt=end_of_month).aggregate(Count('id'))
        kts_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia__gte=start_of_month,
                                     date_otklulchenia__lt=end_of_month).aggregate(Count('id'))
        # 2 podlk
        kts_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                       date_podkluchenia__lt=end_of_month)
        kts_abon_summa_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                                  date_podkluchenia__lt=end_of_month).aggregate(Sum('itog_oplata'))
        kts_count_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                             date_podkluchenia__lt=end_of_month).aggregate(Count('id'))
        kts_fiz_podkl = kts.objects.filter(company_name_id=company.id, urik=False,
                                           date_podkluchenia__gte=start_of_month,
                                           date_podkluchenia__lt=end_of_month).aggregate(Count('id'))
        reports.append({
            'companies': companies, 'urik_companies': urik_companies,
            'non_urik_companies_quantity': non_urik_companies_quantity,
            'kts_otkl': kts_otkl, 'kts_abon_summa': kts_abon_summa,
            'kts_count': kts_count, 'kts_fiz': kts_fiz,
            'kts_podkl': kts_podkl, 'kts_abon_summa_podkl': kts_abon_summa_podkl, 'kts_count_podkl': kts_count_podkl,
            'kts_fiz_podkl': kts_fiz_podkl,
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
        })
        context = {'reports': reports, 'start_of_month': start_of_month, 'end_of_month': end_of_month}
    return render(request, 'dogovornoy/reports.html', context)


# Страница отчеты договорной
@login_required
def reports_agentskie(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month-1, 1, tzinfo=timezone.utc)
    end_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    companies = rekvizity.objects.all()
    urik_companies = rekvizity.objects.filter(kts__urik=True, kts__date_otklulchenia=None)
    non_urik_companies_quantity = rekvizity.objects.filter(kts__urik=False, kts__date_otklulchenia=None)

    reports = []

    for company in companies:
        # 1 otlk
        kts_otkl = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                      date_otklulchenia__lt=end_of_month)
        kts_abon_summa = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lt=end_of_month).aggregate(Sum('abon_plata'))
        kts_count = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                       date_otklulchenia__lt=end_of_month).aggregate(Count('id'))
        kts_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia__gte=start_of_month,
                                     date_otklulchenia__lt=end_of_month).aggregate(Count('id'))
        # 2 podlk
        kts_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                       date_podkluchenia__lt=end_of_month)
        kts_abon_summa_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                                  date_podkluchenia__lt=end_of_month).aggregate(Sum('itog_oplata'))
        kts_count_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                             date_podkluchenia__lt=end_of_month).aggregate(Count('id'))
        kts_fiz_podkl = kts.objects.filter(company_name_id=company.id, urik=False,
                                           date_podkluchenia__gte=start_of_month,
                                           date_podkluchenia__lt=end_of_month).aggregate(Count('id'))
        reports.append({
            'companies': companies, 'urik_companies': urik_companies,
            'non_urik_companies_quantity': non_urik_companies_quantity,
            'kts_otkl': kts_otkl, 'kts_abon_summa': kts_abon_summa,
            'kts_count': kts_count, 'kts_fiz': kts_fiz,
            'kts_podkl': kts_podkl, 'kts_abon_summa_podkl': kts_abon_summa_podkl, 'kts_count_podkl': kts_count_podkl,
            'kts_fiz_podkl': kts_fiz_podkl,
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
        })
        context = {'reports': reports, 'start_of_month': start_of_month, 'end_of_month': end_of_month}
    return render(request, 'dogovornoy/reports_agentskie.html', context)
