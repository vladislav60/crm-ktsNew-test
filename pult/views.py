# pult/views.py
from calendar import *
import re

import now as now
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *
import pandas as pd
from .models import Alarme
from datetime import *



def card_list(request):
    cards = Cards.objects.using('third_db').select_related('unittype', 'basenumber', 'orgid').all()
    return render(request, 'card_list.html', {'cards': cards})


def card_detail(request, pk):
    card = get_object_or_404(Cards.objects.using('third_db').select_related('basenumber', 'unittype', 'orgid'), pk=pk)
    zones = Zones.objects.using('third_db').filter(cardid=pk).select_related('sectionid')
    alarms = Alarme.objects.using('third_db') \
        .filter(zoneid__in=[zone.zoneid for zone in zones]) \
        .select_related('zoneid', 'reason') \
        .order_by('receivetime')

    return render(request, 'card_detail.html', {'card': card, 'zones': zones, 'alarms': alarms})



def alarm_report(request):
    # Get the current date and calculate the start of the current month
    now = datetime.now()
    start_of_month = now.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    yesterday = now - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Filter out alarms where sendtime_deg is empty and within the current month
    alarms = Alarme.objects.using('third_db').exclude(sendtime_deg__isnull=True).select_related('zoneid__cardid', 'reason').filter(receivetime__gte=start_of_month)

    # Prepare data for the report
    data = []
    for alarm in alarms:
        if alarm.receivetime:
            data.append({
                'alarmid': alarm.alarmid,
                'client': alarm.zoneid.cardid.objectname,
                'client_id': alarm.zoneid.cardid.pk,  # Ensure this is correct
                'receivetime': alarm.receivetime,
                'confirmtime': alarm.confirmtime,
                'processtime': alarm.processtime,
                'reason': alarm.reason.name if alarm.reason else 'Unknown',
                'sendtime_deg': alarm.sendtime_deg,
                'receivecount': alarm.receivecount,
                'confirmtime_deg': alarm.confirmtime_deg,
                'receivetime_deg': alarm.receivetime_deg,
                'unitnumber': alarm.zoneid.cardid.unitnumber,
                'otisnumber': alarm.zoneid.cardid.otisnumber,
                'callnumber': alarm.zoneid.cardid.callnumber,
                'callsign': alarm.zoneid.cardid.callsign,
                # 'name_org': alarm.zoneid.cardid.orgid.name,
            })

    # Convert data to DataFrame for analysis
    df = pd.DataFrame(data)

    # Calculate total alarms per client
    total_alarms = df.groupby(['client', 'unitnumber', 'otisnumber', 'client_id', 'callsign']).size().reset_index(name='total_alarms')

    # Calculate average time to confirm and process per client
    df['time_to_confirm'] = (df['confirmtime'] - df['receivetime']).dt.total_seconds() / 60.0
    df['time_to_process'] = (df['processtime'] - df['receivetime']).dt.total_seconds() / 60.0
    avg_times = df.groupby(['client', 'unitnumber', 'otisnumber', 'client_id', 'callsign']).agg({'time_to_confirm': 'mean', 'time_to_process': 'mean'}).reset_index()

    # Identify most common reasons for alarms per client
    common_reasons = df.groupby(['client', 'reason']).size().reset_index(name='reason_count')
    common_reasons = common_reasons.loc[common_reasons.groupby('client')['reason_count'].idxmax()][['client', 'reason']]

    # Filter clients with total_alarms >= 3
    total_alarms = total_alarms[total_alarms['total_alarms'] >= 3]

    # Time of day analysis
    df['hour'] = df['receivetime'].dt.hour
    alarms_by_hour = df.groupby(['client', 'hour']).size().unstack(fill_value=0).reset_index()

    # Merge all data into a single DataFrame
    report = total_alarms.merge(avg_times, on=['client', 'unitnumber', 'otisnumber', 'client_id', 'callsign'], how='left') \
                         .merge(common_reasons, on='client', how='left')

    report = report.fillna(0)

    # Sort the report by total_alarms in descending order
    report = report.sort_values(by='total_alarms', ascending=False)


    # Prepare yesterday's alarms
    yesterdays_alarms = df[(df['receivetime'] >= start_of_yesterday) & (df['receivetime'] <= end_of_yesterday)]
    yesterdays_total_alarms = yesterdays_alarms.groupby('client').size().reset_index(name='yesterday_total_alarms')
    yesterdays_high_risk_clients = yesterdays_total_alarms[yesterdays_total_alarms['yesterday_total_alarms'] >= 3]

    # Merge yesterday's alarms with the high-risk clients
    yesterdays_report = yesterdays_alarms.merge(yesterdays_high_risk_clients, on='client', how='inner')

    df['day'] = df['receivetime'].dt.day

    # Group by callnumber and day to count alarms
    alarm_counts = df.groupby(['callnumber', 'callsign', 'day']).size().unstack(fill_value=0).reset_index()

    # Ensure all days are included as columns
    days_in_month = list(range(1, end_of_month.day + 1))
    alarm_counts = alarm_counts.reindex(columns=['callnumber', 'callsign'] + days_in_month, fill_value=0)

    # Sort the DataFrame by callnumber
    alarm_counts = alarm_counts.sort_values(by='callnumber')


    context = {
        'report': report.to_dict(orient='records'),
        'yesterdays_report': yesterdays_report.to_dict(orient='records'),
        'alarm_counts': alarm_counts.to_dict(orient='records'),
        'days_in_month': list(days_in_month),
    }

    return render(request, 'alarm_report.html', context)



def alarm_report_tech(request):
    # Get the current date and calculate the start of the current month
    now = datetime.now()
    start_of_month = now.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    yesterday = now - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    reason_codes = [0, 1, 2, 4, 6, 11, 13, 14, 15, 17]

    # Filter out alarms where sendtime_deg is empty and within the current month
    alarms = Alarme.objects.using('third_db').exclude(sendtime_deg__isnull=True).select_related('zoneid__cardid', 'reason').filter(receivetime__gte=start_of_month, reason__in=reason_codes)

    # Prepare data for the report
    data = []
    for alarm in alarms:
        if alarm.receivetime:
            # Extract the 'Уч' value from the 'info' column
            info = alarm.zoneid.cardid.info
            match = re.search(r'Уч\.(\d+)', info)
            uchastok = match.group(0) if match else 'Unknown'

            data.append({
                'alarmid': alarm.alarmid,
                'client': alarm.zoneid.cardid.objectname,
                'client_id': alarm.zoneid.cardid.pk,
                'receivetime': alarm.receivetime,
                'confirmtime': alarm.confirmtime,
                'processtime': alarm.processtime,
                'reason': alarm.reason.name if alarm.reason else 'Unknown',
                'sendtime_deg': alarm.sendtime_deg,
                'receivecount': alarm.receivecount,
                'confirmtime_deg': alarm.confirmtime_deg,
                'receivetime_deg': alarm.receivetime_deg,
                'unitnumber': alarm.zoneid.cardid.unitnumber,
                'otisnumber': alarm.zoneid.cardid.otisnumber,
                'callnumber': alarm.zoneid.cardid.callnumber,
                'callsign': alarm.zoneid.cardid.callsign,
                'uchastok': uchastok,
            })

    # Convert data to DataFrame for analysis
    df = pd.DataFrame(data)

    # Group and count alarms by 'участок'
    alarms_by_uchastok = df.groupby('uchastok').size().reset_index(name='total_alarms')

    context = {
        'alarms_by_uchastok': alarms_by_uchastok.to_dict(orient='records'),
    }

    return render(request, 'alarm_report_tech.html', context)


def export_alarms_to_excel(request):
    # Get the current date and calculate the start of the current month
    now = datetime.now()
    start_of_month = now.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    yesterday = now - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    reason_codes = [0, 1, 2, 4, 6, 11, 13, 14, 15, 17]

    # Filter out alarms where sendtime_deg is empty and within the current month
    alarms = Alarme.objects.using('third_db').exclude(sendtime_deg__isnull=True).select_related('zoneid__cardid', 'reason').filter(receivetime__gte=start_of_month, reason__in=reason_codes)

    # Собираем данные в список словарей
    data = [{
        'Alarm ID': alarm.alarmid,
        'unitnumber': alarm.zoneid.cardid.unitnumber,
        'otisnumber': alarm.zoneid.cardid.otisnumber,
        'Client Name': alarm.zoneid.cardid.objectname,
        'Client Info': alarm.zoneid.cardid.info,
        'Receive Time': alarm.receivetime,
        'Confirm Time': alarm.confirmtime,
        'Process Time': alarm.processtime,
        'confirmtime': alarm.confirmtime,
        'processtime': alarm.processtime,
        'reason': alarm.reason.name if alarm.reason else 'Unknown',
        'sendtime_deg': alarm.sendtime_deg,
        'receivecount': alarm.receivecount,
        'confirmtime_deg': alarm.confirmtime_deg,
        'receivetime_deg': alarm.receivetime_deg,
    } for alarm in alarms]

    # Преобразуем список словарей в DataFrame
    df = pd.DataFrame(data)

    # Создаем файл Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="alarms.xlsx"'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response
















