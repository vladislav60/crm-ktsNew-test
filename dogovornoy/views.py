import calendar
import math
from io import BytesIO

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

from ktscrm import settings
from .forms import ExcelImportForm
from .models import *
import numpy as np
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.utils.dateparse import parse_date
import openpyxl
from openpyxl.utils import get_column_letter
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

        additional_services_cost = passport_info.additional_services.aggregate(total_cost=Sum('price'))['total_cost']
        itog_oplata = passport_info.abon_plata + (additional_services_cost or 0)
        rekvizity_test = rekvizity.objects.get(pk=passport_info.company_name_id)
        current_date = date.today()
        current_date = current_date.strftime("%d/%m/%Y")
        currency_main = ('тенге', 'тенге', 'тенге')
        currency_additional = ('тиын', 'тиына', 'тиынов')
        itog_oplata_propis = get_string_by_number(itog_oplata, currency_main, currency_additional)
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
            'mat_otv': (passport_info.mat_otv or 0),
            'mat_otv_itog1': mat_otv_itog2,
            'itog_oplata': itog_oplata,
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


@method_decorator(login_required, name='dispatch')
class AddClientPartner(FormView):
    template_name = 'dogovornoy/add_client_partner.html'
    form_class = AddKlientDogFormPartner
    success_url = '/baza_partnerov/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, menu=menu, title='Новый клиент партнеров'))


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
def update_client_partner(request, partner_klient_id):
    kartochka_partner = get_object_or_404(partners_object, pk=partner_klient_id)
    if request.method == 'POST':
        form = AddKlientDogFormPartner(request.POST, request.FILES, instance=kartochka_partner)
        if form.is_valid():
            form.save()
            return redirect('baza_partnerov')
    else:
        form = AddKlientDogFormPartner(instance=kartochka_partner)

    return render(request, 'dogovornoy/update_client_partner.html', {'form': form, 'kartochka_partner': kartochka_partner})


@login_required
def delete_client(request, klient_id):
    kartochka = get_object_or_404(kts, pk=klient_id)
    if request.method == 'POST':
        kartochka.delete()
        return redirect('baza_dogovorov')
    return render(request, 'dogovornoy/delete_client.html', {'kartochka': kartochka})


@login_required
def delete_client_partners(request, partner_klient_id):
    kartochka_partner = get_object_or_404(partners_object, pk=partner_klient_id)
    if request.method == 'POST':
        kartochka_partner.delete()
        return redirect('baza_partnerov')
    return render(request, 'dogovornoy/delete_client.html', {'kartochka_partner': kartochka_partner})


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

        return render(request, self.template_name,
                      {'klienty': page_obj, 'company_names': company_names,
                       'pagination_url': pagination_url, 'total_entries': queryset.count()})


@method_decorator(login_required, name='dispatch')
class DogBazaPartners(ListView):
    model = partners_object
    template_name = 'dogovornoy/baza_partnerov.html'
    context_object_name = 'klienty_partners'

    def get(self, request, *args, **kwargs):
        queryset = partners_object.objects.all()
        query = self.request.GET.get('q')
        company_partners = partners_rekvizity.objects.values_list('id', 'polnoe_name')
        object_number = self.request.GET.get('object_number')
        company_name = self.request.GET.get('company_name')
        gsm_number = self.request.GET.get('gsm_number')

        if query:
            queryset = queryset.filter(
                Q(object_number__icontains=query) |
                Q(gsm_number__icontains=query) |
                Q(name_object__icontains=query) |
                Q(adres__icontains=query)
            )

        if object_number:
            queryset = queryset.filter(object_number__icontains=object_number)
        if company_name:
            queryset = queryset.filter(company_name_id__exact=company_name)
        if gsm_number:
            queryset = queryset.filter(gsm_number__icontains=gsm_number)

        paginator = Paginator(queryset, per_page=25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        params = request.GET.copy()
        if 'page' in params:
            del params['page']
        pagination_url = request.path + '?' + urlencode(params)

        return render(request, self.template_name,
                      {'klienty_partners': page_obj, 'company_partners': company_partners,
                       'pagination_url': pagination_url, 'total_entries': queryset.count()})


@method_decorator(login_required, name='dispatch')
class Rekvizity(ListView):
    model = rekvizity
    template_name = 'dogovornoy/rekvizity.html'
    context_object_name = 'rekvizity'


@method_decorator(login_required, name='dispatch')
class RekvizityPartners(ListView):
    model = partners_rekvizity
    context_object_name = 'partners_rekvizity'

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


@login_required
def partnerts_importexel(request):
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
                partners_obj = partners_object(
                    object_number=row['object_number'],
                    gsm_number=row['gsm_number'],
                    name_object=row['name_object'],
                    adres=row['adres'],
                    type_object=row['type_object'],
                    hours_mounth=row['hours_mounth'],
                    date_podkluchenia=row['date_podkluchenia'],
                    tariff_per_mounth=row['tariff_per_mounth'],
                    tehnical_services=row['tehnical_services'],
                    rent_gsm=row['rent_gsm'],
                    fire_alarm=row['fire_alarm'],
                    telemetria=row['telemetria'],
                    nabludenie=row['nabludenie'],
                    sms_uvedomlenie=row['sms_uvedomlenie'],
                    kolvo_day=row['kolvo_day'],
                    primechanie=row['primechanie'],
                    urik=row['urik'],
                    company_name_id=row['company_name_id'],
                    ekipazh_id=row['ekipazh_id'],
                    vid_sign_id=row['vid_sign_id'],
                    date_otkluchenia=row['date_otkluchenia'],
                )
                partners_obj.save()

            # Redirect to the kts list page
            return HttpResponseRedirect(reverse('baza_partnerov'))
    else:
        form = PartnersImportForm()

    return render(request, 'dogovornoy/partnerts_importexel.html', {'form': form})


@login_required
def importrekvizity(request):
    if request.method == 'POST':
        form = RekvizityImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['excel_file']

            # Load the Excel data into a Pandas dataframe
            df = pd.read_excel(excel_file)
            df = df.replace({np.nan: None})
            print(df)
            # Iterate over the rows of the dataframe and create kts objects
            for index, row in df.iterrows():
                rekvizity_obj = rekvizity(
                    id=row['id'],
                    polnoe_name=row['polnoe_name'],
                    adres_company=row['adres_company'],
                    bin=row['bin'],
                    iban=row['iban'],
                    bic=row['bic'],
                    bank=row['bank'],
                    telephone_ofiice=row['telephone_ofiice'],
                    telephone_buh=row['telephone_buh'],
                    vid_too=row['vid_too'],
                    doljnost=row['doljnost'],
                    ucheriditel_name_polnoe=row['ucheriditel_name_polnoe'],
                    ucheriditel_name_sokr=row['ucheriditel_name_sokr'],
                )
                rekvizity_obj.save()

            # Redirect to the kts list page
            return HttpResponseRedirect(reverse('rekvizity'))
    else:
        form = RekvizityImportForm()

    return render(request, 'dogovornoy/importrekvizity.html', {'form': form})


@login_required
def importvidsign(request):
    if request.method == 'POST':
        form = VidSignImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['excel_file']

            # Load the Excel data into a Pandas dataframe
            df = pd.read_excel(excel_file)
            df = df.replace({np.nan: None})
            print(df)
            # Iterate over the rows of the dataframe and create kts objects
            for index, row in df.iterrows():
                vidsign_obj = vid_sign(
                    id=row['id'],
                    name_sign=row['name_sign'],
                    name_sign_polnoe=row['name_sign_polnoe'],
                )
                vidsign_obj.save()

            # Redirect to the kts list page
            return HttpResponseRedirect(reverse('baza_dogovorov'))
    else:
        form = VidSignImportForm()

    return render(request, 'dogovornoy/importvidsign.html', {'form': form})


@login_required
def importekipazh(request):
    if request.method == 'POST':
        form = VidSignImportForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['excel_file']

            # Load the Excel data into a Pandas dataframe
            df = pd.read_excel(excel_file)
            df = df.replace({np.nan: None})
            print(df)
            # Iterate over the rows of the dataframe and create kts objects
            for index, row in df.iterrows():
                ekipazh_obj = ekipazh(
                    id=row['id'],
                    ekipazh_name=row['ekipazh_name'],
                )
                ekipazh_obj.save()

            # Redirect to the kts list page
            return HttpResponseRedirect(reverse('baza_dogovorov'))
    else:
        form = EkipazhImportForm()

    return render(request, 'dogovornoy/importekipazh.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class KartochkaKlienta(DetailView):
    model = kts
    template_name = 'dogovornoy/kartochka_klienta.html'
    pk_url_kwarg = 'klient_id'
    context_object_name = 'kartochka'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kts_instance = self.get_object()
        additional_services_cost = kts_instance.additional_services.aggregate(total_cost=Sum('price'))['total_cost']
        itog_oplata = kts_instance.abon_plata + (additional_services_cost or 0)
        context['itog_oplata'] = itog_oplata
        context['form'] = AdditionalServiceForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AdditionalServiceForm(request.POST)
        if form.is_valid():
            kts_instance = self.get_object()  # Get the Kts instance associated with the view
            form.instance.kts = kts_instance  # Associate the additional service with the Kts instance
            form.save()  # Save the additional service
            return redirect('kartochka_klienta', klient_id=kts_instance.pk)
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class KartochkaPartner(DetailView):
    model = partners_object
    template_name = 'dogovornoy/kartochka_partner.html'
    pk_url_kwarg = 'partner_klient_id'
    context_object_name = 'kartochka_partner'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        partner_object = self.get_object()
        num_days_mounth = calendar.monthrange(now.year, now.month)[1]

        start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
        end_of_month = datetime(now.year, now.month, num_days_mounth, tzinfo=timezone.utc).date()

        if partner_object.date_otkluchenia:
            if (partner_object.date_otkluchenia > start_of_month) and (
                    partner_object.date_podkluchenia < start_of_month):
                num_days = (partner_object.date_otkluchenia - start_of_month).days
            elif (partner_object.date_otkluchenia > start_of_month) and (partner_object.date_podkluchenia >= start_of_month):
                num_days = (partner_object.date_otkluchenia - partner_object.date_podkluchenia).days
            elif partner_object.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (partner_object.date_podkluchenia - partner_object.date_otkluchenia).days
            else:
                num_days = (partner_object.date_otkluchenia - start_of_month).days
        else:
            if partner_object.date_podkluchenia > start_of_month:
                num_days = (end_of_month - partner_object.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        # Calculate itog_tehnical_services
        if partner_object.tehnical_services:
            if partner_object.urik:
                itog_tehnical_services = int(
                    (partner_object.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days)
            else:
                itog_tehnical_services = int(
                    (partner_object.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days)
        else:
            itog_tehnical_services = 0

        if partner_object.rent_gsm:
            if partner_object.urik:
                itog_rent_gsm = int((partner_object.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((partner_object.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0


        if partner_object.fire_alarm:
            if partner_object.urik:
                itog_fire_alarm = int((partner_object.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((partner_object.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0


        if partner_object.telemetria:
            itog_telemetria = int((partner_object.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if partner_object.nabludenie:
            if partner_object.urik:
                itog_nabludenie = int((partner_object.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((partner_object.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if partner_object.sms_uvedomlenie:
            sms_uvedomlenie = partner_object.company_name.sms
            if partner_object.sms_number:
                itog_sms_uvedomlenie = int(
                    ((partner_object.company_name.sms * partner_object.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((partner_object.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0


        # Calculate reagirovanie
        if partner_object.urik:
            reagirovanie = (partner_object.hours_mounth * partner_object.tariff_per_mounth) / num_days_mounth * num_days
        else:
            reagirovanie = (partner_object.tariff_per_mounth / num_days_mounth) * num_days

        reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
            reagirovanie)


        if partner_object.primechanie == '50% на 50%':
            summ_mounth = int((itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm) / 2)
        else:
            summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm


        context['itog_tehnical_services'] = itog_tehnical_services
        context['reagirovanie'] = reagirovanie
        context['num_days'] = num_days
        context['itog_rent_gsm'] = itog_rent_gsm
        context['itog_fire_alarm'] = itog_fire_alarm
        context['itog_telemetria'] = itog_telemetria
        context['itog_nabludenie'] = itog_nabludenie
        context['itog_sms_uvedomlenie'] = itog_sms_uvedomlenie
        context['sms_uvedomlenie'] = sms_uvedomlenie
        context['summ_mounth'] = summ_mounth

        return context

@login_required
def delete_additional_service(request, service_id):
    additional_service = get_object_or_404(AdditionalService, pk=service_id)

    if request.method == 'POST':
        additional_service.delete()
        return redirect('baza_dogovorov')  # Redirect to client list or a specific page after deletion

    return render(request, 'dogovornoy/delete_additional_service.html', {'additional_service': additional_service})


@login_required
def edit_additional_service(request, service_id):
    additional_service = get_object_or_404(AdditionalService, pk=service_id)

    if request.method == 'POST':
        form = AdditionalServiceForm(request.POST, instance=additional_service)
        if form.is_valid():
            form.save()
            return redirect('baza_dogovorov')  # Redirect to client list or a specific page after editing
    else:
        form = AdditionalServiceForm(instance=additional_service)

    return render(request, 'dogovornoy/edit_additional_service.html',
                  {'form': form, 'additional_service': additional_service})


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
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = timezone.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)

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
        kts_otkl = kts.objects.filter(
            Q(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
              date_otklulchenia__lte=end_of_month, exclude_from_report=False) |
            Q(company_name_id=company.id, additional_services__date_unsubscribe__gte=start_of_month,
              additional_services__date_unsubscribe__lte=end_of_month, exclude_from_report=False)
        ).distinct()
        kts_abon_summa_otkl = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month).aggregate(Sum('abon_plata'))
        kts_count = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                       date_otklulchenia__lte=end_of_month).aggregate(Count('id'))
        kts_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia__gte=start_of_month,
                                     date_otklulchenia__lte=end_of_month).aggregate(Count('id'))

        # 2 podlk
        kts_podkl = kts.objects.filter(
            Q(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
              date_podkluchenia__lte=end_of_month, exclude_from_report=False) |
            Q(company_name_id=company.id, additional_services__date_added__gte=start_of_month,
              additional_services__date_added__lte=end_of_month, exclude_from_report=False)
        ).distinct()

        kts_abon_summa_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                                  date_podkluchenia__lte=end_of_month).aggregate(Sum('abon_plata'))

        kts_count_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                             date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        kts_fiz_podkl = kts.objects.filter(company_name_id=company.id, urik=False,
                                           date_podkluchenia__gte=start_of_month,
                                           date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        # 2 Все объекты до выбранной даты
        kts_podkl_dodate = kts.objects.filter(company_name_id=company.id, date_podkluchenia__lte=end_of_month,
                                       date_otklulchenia=None, urik=True, exclude_from_report=False)


        # Всего на начало выбранного месяцаkolvo_podkl_fiz
        kts_count_podkl_alldate = kts.objects.filter(company_name_id=company.id,date_podkluchenia__lte=start_of_month,
                                                     date_otklulchenia=None,exclude_from_report=False).aggregate(Count('id'))


        kts_count_podkl_kv_stmth = kts.objects.filter(company_name_id=company.id, date_podkluchenia__lte=start_of_month,
                                                     date_otklulchenia=None, name_object="квартира",
                                                      exclude_from_report=False).aggregate(Count('id'))

        kts_count_podkl_dom_stmth = kts.objects.filter(company_name_id=company.id, date_podkluchenia__lte=start_of_month,
                                                      date_otklulchenia=None, name_object="дом",
                                                      exclude_from_report=False).aggregate(Count('id'))

        kts_fiz_podkl_startdate = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia=None,
                                           date_podkluchenia__lte=start_of_month, exclude_from_report=False).aggregate(Count('id'))

        kts_ur_podkl_startdate = kts.objects.filter(company_name_id=company.id, urik=True, date_otklulchenia=None,
                                                     date_podkluchenia__lte=start_of_month,
                                                     exclude_from_report=False).aggregate(Count('id'))

        # Всего на конец выбранного месяца
        kts_count_podkl_end = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None, urik=True,
                                                 date_podkluchenia__lte=end_of_month,
                                                 exclude_from_report=False).aggregate(Count('id'))

        kts_fiz_podkl_end = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia=None,
                                               date_podkluchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        kts_podkl_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                               date_podkluchenia__lte=end_of_month,
                                               exclude_from_report=False).aggregate(Count('id'))

        kts_podkl_kv_end_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                           date_podkluchenia__lte=end_of_month,name_object="квартира",
                                           exclude_from_report=False).aggregate(Count('id'))

        kts_podkl_dom_end_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                  date_podkluchenia__lte=end_of_month, name_object="дом",
                                                  exclude_from_report=False).aggregate(Count('id'))

        # принято(в т.ч.после вр.снятия )
        kolvo_podkl_obj_urik = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                             date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                             date_podkluchenia__lte=end_of_month, urik=True).aggregate(Count('id'))

        kolvo_podkl_obj_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia=None,
                                             date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                             date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        kolvo_podkl_obj_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                 date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                                 date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        kolvo_podkl_obj_kv = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                 date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                                 date_podkluchenia__lte=end_of_month,name_object="квартира").aggregate(Count('id'))

        kolvo_podkl_obj_dom = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                                date_podkluchenia__lte=end_of_month, name_object="дом").aggregate(Count('id'))

        # расторженно (в т.ч.после вр.снятия )
        kolvo_otkl_obj = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        kolvo_otkl_fiz = kts.objects.filter(company_name_id=company.id, urik=False,
                                            date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        # экипажи физические лица
        gruppa_reagirovania_911_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=False, gruppa_reagirovania='911',date_podkluchenia__lte=end_of_month,
                                                         exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_bravo21_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                             urik=False, gruppa_reagirovania='Браво-21',date_podkluchenia__lte=end_of_month,
                                                             exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_sms_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=False, gruppa_reagirovania='СМС',date_podkluchenia__lte=end_of_month,
                                                         exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_asker_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                           urik=False, gruppa_reagirovania='Әскер',date_podkluchenia__lte=end_of_month,
                                                           exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_zardem_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                            urik=False, gruppa_reagirovania='Жардем',date_podkluchenia__lte=end_of_month,
                                                            exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_kuguar_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                            urik=False, gruppa_reagirovania='Кугуар',
                                                            date_podkluchenia__lte=end_of_month,
                                                            exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_kapchagai_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                            urik=False, gruppa_reagirovania='Капшагай',
                                                            date_podkluchenia__lte=end_of_month,
                                                            exclude_from_report=False).aggregate(Count('id'))

        # экипажи юридические лица
        gruppa_reagirovania_911_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        urik=True, date_podkluchenia__lte=end_of_month,
                                                        gruppa_reagirovania='911').aggregate(Count('id'))

        gruppa_reagirovania_bravo21_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                            urik=True, gruppa_reagirovania='Браво-21',
                                                            date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_sms_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        urik=True, gruppa_reagirovania='СМС',
                                                        date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_asker_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                          urik=True, gruppa_reagirovania='Эскер',
                                                          date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_zardem_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                           urik=True, gruppa_reagirovania='Жардем',
                                                           date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_kapchagai_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                               urik=True, gruppa_reagirovania='Капшагай',
                                                               date_podkluchenia__lte=end_of_month,
                                                               exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_kuguar_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                              urik=True, gruppa_reagirovania='Кугуар',
                                                              date_podkluchenia__lte=end_of_month,
                                                              exclude_from_report=False).aggregate(Count('id'))


        # Итого для юридические лицаЭкипажи
        gruppa_reagirovania_911_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        date_podkluchenia__lte=end_of_month,
                                                        gruppa_reagirovania='911').aggregate(Count('id'))

        gruppa_reagirovania_bravo21_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                            gruppa_reagirovania='Браво-21',
                                                            date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_sms_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        gruppa_reagirovania='СМС',
                                                        date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_asker_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                          gruppa_reagirovania='Эскер',
                                                          date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_zardem_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                           gruppa_reagirovania='Жардем',
                                                           date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        gruppa_reagirovania_kapchagai_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                              gruppa_reagirovania='Капшагай',date_podkluchenia__lte=end_of_month,
                                                              exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_kuguar_all = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                           gruppa_reagirovania='Кугуар',
                                                           date_podkluchenia__lte=end_of_month,
                                                           exclude_from_report=False).aggregate(Count('id'))

        print(kts_count_podkl)
        # 2 podlk
        for kts_instance in kts_podkl:
            # Calculate the total cost of additional services for each kts_instance
            additional_services_cost = kts_instance.additional_services.aggregate(total_cost=Sum('price'))['total_cost']
            additional_services_prim = kts_instance.additional_services.all()
            for service in additional_services_prim:
                kts_instance.primechanie = f"{kts_instance.primechanie}, '{service.service_name}' c '{service.date_added}' а/п была = {kts_instance.abon_plata or 0} "

            if additional_services_cost:
                if kts_instance.date_podkluchenia.month != start_of_month.month:
                    kts_instance.abon_plata = additional_services_cost
                    kts_abon_summa_podkl['abon_plata__sum'] = (kts_abon_summa_podkl['abon_plata__sum'] or 0) + additional_services_cost
                else:
                    kts_instance.abon_plata = kts_instance.abon_plata + additional_services_cost
                    kts_abon_summa_podkl['abon_plata__sum'] = kts_abon_summa_podkl['abon_plata__sum'] + additional_services_cost

        # 1 otlk
        for kts_instance in kts_otkl:
            # Calculate the total cost of additional services for each kts_instance
            additional_services_cost = kts_instance.additional_services.aggregate(total_cost=Sum('price'))['total_cost']
            additional_services_prim = kts_instance.additional_services.all()
            for service in additional_services_prim:
                kts_instance.primechanie = f"{kts_instance.primechanie}, '{service.service_name}' c '{service.date_unsubscribe}' а/п была = {kts_instance.abon_plata or 0} "

            if additional_services_cost:
                if kts_instance.date_otklulchenia.month != start_of_month.month:
                    kts_instance.abon_plata = additional_services_cost
                else:
                    kts_instance.abon_plata = kts_instance.abon_plata + additional_services_cost
                    kts_abon_summa_otkl['abon_plata__sum'] = kts_abon_summa_otkl['abon_plata__sum'] + additional_services_cost

        reports.append({
            'companies': companies,
            'urik_companies': urik_companies,
            'non_urik_companies_quantity': non_urik_companies_quantity,
            'kts_otkl': kts_otkl,
            'kts_count': kts_count, 'kts_fiz': kts_fiz,
            'kts_podkl': kts_podkl,
            'kts_abon_summa_podkl': kts_abon_summa_podkl,
            'kts_abon_summa_otkl': kts_abon_summa_otkl,
            'kts_count_podkl': kts_count_podkl,
            'kts_fiz_podkl': kts_fiz_podkl,
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
            'end_of_month': end_of_month,
            'kts_podkl_dodate': kts_podkl_dodate,
            'kolvo_podkl_obj_urik': kolvo_podkl_obj_urik,
            'kolvo_podkl_obj_fiz': kolvo_podkl_obj_fiz,
            'kts_count_podkl_kv_stmth' : kts_count_podkl_kv_stmth,
            'kts_count_podkl_dom_stmth' : kts_count_podkl_dom_stmth,
            'kolvo_otkl_obj': kolvo_otkl_obj,
            'kolvo_otkl_fiz': kolvo_otkl_fiz,
            'gruppa_reagirovania_911_fiz': gruppa_reagirovania_911_fiz,
            'gruppa_reagirovania_sms_fiz': gruppa_reagirovania_sms_fiz,
            'gruppa_reagirovania_asker_fiz': gruppa_reagirovania_asker_fiz,
            'gruppa_reagirovania_zardem_fiz': gruppa_reagirovania_zardem_fiz,
            'gruppa_reagirovania_bravo21_fiz': gruppa_reagirovania_bravo21_fiz,
            'gruppa_reagirovania_911_ur': gruppa_reagirovania_911_ur,
            'gruppa_reagirovania_sms_ur': gruppa_reagirovania_sms_ur,
            'gruppa_reagirovania_asker_ur': gruppa_reagirovania_asker_ur,
            'gruppa_reagirovania_zardem_ur': gruppa_reagirovania_zardem_ur,
            'gruppa_reagirovania_bravo21_ur': gruppa_reagirovania_bravo21_ur,
            'kts_count_podkl_end': kts_count_podkl_end,
            'kts_fiz_podkl_end': kts_fiz_podkl_end,
            'kts_count_podkl_alldate': kts_count_podkl_alldate,
            'kts_fiz_podkl_startdate' : kts_fiz_podkl_startdate,
            'kts_ur_podkl_startdate' : kts_ur_podkl_startdate,
            'kolvo_podkl_obj_all':kolvo_podkl_obj_all,
            'kolvo_podkl_obj_kv':kolvo_podkl_obj_kv,
            'kolvo_podkl_obj_dom':kolvo_podkl_obj_dom,
            'kts_podkl_all':kts_podkl_all,
            'kts_podkl_kv_end_all':kts_podkl_kv_end_all,
            'kts_podkl_dom_end_all':kts_podkl_dom_end_all,
            'gruppa_reagirovania_kuguar_fiz':gruppa_reagirovania_kuguar_fiz,
            'gruppa_reagirovania_kapchagai_fiz':gruppa_reagirovania_kapchagai_fiz,
            'gruppa_reagirovania_kapchagai_ur':gruppa_reagirovania_kapchagai_ur,
            'gruppa_reagirovania_kuguar_ur':gruppa_reagirovania_kuguar_ur,
            'gruppa_reagirovania_sms_all':gruppa_reagirovania_sms_all,
            'gruppa_reagirovania_bravo21_all':gruppa_reagirovania_bravo21_all,
            'gruppa_reagirovania_zardem_all':gruppa_reagirovania_zardem_all,
            'gruppa_reagirovania_911_all':gruppa_reagirovania_911_all,
            'gruppa_reagirovania_kapchagai_all':gruppa_reagirovania_kapchagai_all,
            'gruppa_reagirovania_kuguar_all':gruppa_reagirovania_kuguar_all,
            'gruppa_reagirovania_asker_all':gruppa_reagirovania_asker_all,

        })
        context = {'reports': reports, 'start_of_month': start_of_month, 'end_of_month': end_of_month}
    return render(request, 'dogovornoy/reports.html', context)


# Страница отчеты договорной
@login_required
def reports_agentskie(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = timezone.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)

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
                                      date_otklulchenia__lte=end_of_month)
        kts_abon_summa = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month).aggregate(Sum('abon_plata'))
        kts_count = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                       date_otklulchenia__lte=end_of_month).aggregate(Count('id'))
        kts_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia__gte=start_of_month,
                                     date_otklulchenia__lte=end_of_month).aggregate(Count('id'))
        # 2 podlk
        kts_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                       date_podkluchenia__lte=end_of_month)
        kts_abon_summa_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                                  date_podkluchenia__lte=end_of_month).aggregate(Sum('abon_plata'))
        kts_count_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__gte=start_of_month,
                                             date_podkluchenia__lte=end_of_month).aggregate(Count('id'))
        kts_fiz_podkl = kts.objects.filter(company_name_id=company.id, urik=False,
                                           date_podkluchenia__gte=start_of_month,
                                           date_podkluchenia__lte=end_of_month).aggregate(Count('id'))
        reports.append({
            'companies': companies,
            'urik_companies': urik_companies,
            'non_urik_companies_quantity': non_urik_companies_quantity,
            'kts_otkl': kts_otkl,
            'kts_abon_summa': kts_abon_summa,
            'kts_count': kts_count,
            'kts_fiz': kts_fiz,
            'kts_podkl': kts_podkl,
            'kts_abon_summa_podkl': kts_abon_summa_podkl,
            'kts_count_podkl': kts_count_podkl,
            'kts_fiz_podkl': kts_fiz_podkl,
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
        })
        context = {'reports': reports, 'start_of_month': start_of_month, 'end_of_month': end_of_month}
    return render(request, 'dogovornoy/reports_agentskie.html', context)

@login_required
def reports_partners(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=1)

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days)
            else:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = int(((kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth) * num_days)
        else:
            reagirovanie = int(kts_instance.tariff_per_mounth)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
    }

    return render(request, 'dogovornoy/reports_partners.html', context)


@login_required
def reports_partners_download_urik(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=1, urik=True)

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days)
            else:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = int(((kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth) * num_days)
        else:
            reagirovanie = int(kts_instance.tariff_per_mounth)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services
        summ_all_company = summ_kts + summ_senim

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
            'summ_all_company': summ_all_company,
        })

    template_path = os.path.join(settings.MEDIA_ROOT, 'reports_partner_sgsplus_urik.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 11
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'I{row_num}'] = report['num_days']
        ws[f'J{row_num}'] = report['itog_telemetria']
        ws[f'K{row_num}'] = report['itog_rent_gsm']
        ws[f'L{row_num}'] = report['itog_nabludenie']
        ws[f'M{row_num}'] = report['reagirovanie']
        ws[f'N{row_num}'] = report['itog_tehnical_services']
        ws[f'O{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'Q{row_num}'] = report['summ_mounth']
        ws[f'R{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+3}'] = 'Итого'
    ws[f'J{row_num+3}'] = report['summ_telemetria']
    ws[f'K{row_num+3}'] = report['summ_rent_gsm']
    ws[f'L{row_num+3}'] = report['summ_nabludenie']
    ws[f'M{row_num+3}'] = report['summ_reagirovanie']
    ws[f'N{row_num+3}'] = report['summ_tehnical_services']
    ws[f'O{row_num+3}'] = report['summ_sms_uvedomlenie']
    ws[f'P{row_num+3}'] = report['summ_fire_alarm']
    ws[f'Q{row_num+3}'] = report['itog_summ_mounth']
    ws[f'C{row_num+6}'] = 'Итого охраняется:'
    ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    ws[f'D{row_num+9}'] = report['summ_senim']
    ws[f'D{row_num+8}'] = report['summ_kts']
    ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'F{row_num+6}'] = report['num_days_mounth']
    ws[f'C{row_num+10}'] = 'Итого к оплате за май 2024г..:'
    ws[f'J{row_num+10}'] = report['summ_all_company']
    ws[f'C{row_num+11}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num+12}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num+12}'] = '___________________'
    ws[f'E{row_num+12}'] = 'Рассказчикова Н.Н.'
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=СГС-Плюс ЮР.xlsx'

    return response


@login_required
def sgs_plus_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=1, urik=False)

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days)
            else:
                itog_tehnical_services = int(
                    (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = int(((kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth) * num_days)
        else:
            reagirovanie = int(kts_instance.tariff_per_mounth)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services
        summ_all_company = summ_kts + summ_senim

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
            'summ_all_company': summ_all_company,
        })

    template_path = os.path.join(settings.MEDIA_ROOT, 'sgs_plus_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        # ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'F{row_num}'] = report['kts_instance'].date_podkluchenia
        # ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'G{row_num}'] = report['num_days']
        ws[f'H{row_num}'] = report['itog_rent_gsm']
        ws[f'I{row_num}'] = report['itog_telemetria']
        ws[f'J{row_num}'] = report['itog_nabludenie']
        ws[f'K{row_num}'] = report['reagirovanie']
        ws[f'L{row_num}'] = report['itog_tehnical_services']
        ws[f'M{row_num}'] = report['itog_sms_uvedomlenie']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'N{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+1}'] = 'Итого'
    ws[f'I{row_num+1}'] = report['summ_telemetria']
    ws[f'H{row_num+1}'] = report['summ_rent_gsm']
    ws[f'J{row_num+1}'] = report['summ_nabludenie']
    ws[f'K{row_num+1}'] = report['summ_reagirovanie']
    ws[f'L{row_num+1}'] = report['summ_tehnical_services']
    ws[f'M{row_num+1}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'N{row_num+1}'] = report['itog_summ_mounth']
    ws[f'C{row_num+2}'] = 'Итого охраняется:'
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'G{row_num+2}'] = report['num_days_mounth']
    ws[f'C{row_num+3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'I{row_num+3}'] = report['summ_all_company']
    ws[f'C{row_num+4}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num+5}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num+5}'] = '___________________'
    ws[f'E{row_num+5}'] = 'Рассказчикова Н.Н.'
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=СГС-Плюс Физ.xlsx'

    return response


# ОТЧЕТЫ АКМ ЭКСЕЛЬ ЭКСПОРТ ПО ФИЗИКАИ И ЮРИКАМ ОТДЕЛЬНО
@login_required
def reports_partners_akm(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=2)

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
    }

    return render(request, 'dogovornoy/reports_partners_akm.html', context)


@login_required
def akm_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=2, urik=False)
    akm_fiz_count = partners_object.objects.filter(company_name_id=2, urik=False).aggregate(Count('id'))
    akm_fiz_count = akm_fiz_count['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'akm_fiz_count': akm_fiz_count,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'akm_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['all_object_number']
        ws[f'D{row_num}'] = report['kts_instance'].name_object
        ws[f'E{row_num}'] = report['kts_instance'].adres
        ws[f'F{row_num}'] = report['kts_instance'].type_object
        ws[f'G{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'H{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'I{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'J{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'K{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'M{row_num}'] = report['itog_tehnical_services']
        ws[f'N{row_num}'] = report['itog_sms_uvedomlenie']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'D{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    ws[f'L{row_num}'] = report['summ_reagirovanie']
    ws[f'M{row_num}'] = report['summ_tehnical_services']
    ws[f'N{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'O{row_num}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    ws[f'G{row_num + 2}'] = report['akm_fiz_count']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'J{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'J{row_num + 5}'] = '___________________'
    ws[f'M{row_num + 5}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO AKM Fiziki {now.date()}.xlsx'

    return response


@login_required
def akm_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=2, urik=True)
    akm_fiz_count = partners_object.objects.filter(company_name_id=2, urik=True).aggregate(Count('id'))
    akm_fiz_count = akm_fiz_count['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'akm_fiz_count': akm_fiz_count,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'akm_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        ws[f'K{row_num}'] = report['reagirovanie']
        ws[f'L{row_num}'] = report['itog_tehnical_services']
        ws[f'M{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'N{row_num}'] = report['itog_fire_alarm']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'D{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    ws[f'K{row_num}'] = report['summ_reagirovanie']
    ws[f'L{row_num}'] = report['summ_tehnical_services']
    ws[f'M{row_num}'] = report['summ_sms_uvedomlenie']
    ws[f'N{row_num}'] = report['summ_fire_alarm']
    ws[f'O{row_num}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    ws[f'G{row_num + 2}'] = report['akm_fiz_count']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'I{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'I{row_num + 5}'] = '___________________'
    ws[f'O{row_num + 5}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO AKM Uriki {now.date()}.xlsx'

    return response

# ОТЧЕТЫ АКМ КОНЕЦ


# ОТЧЕТЫ RMG ЭКСЕЛЬ ЭКСПОРТ ПО ФИЗИКАИ И ЮРИКАМ ОТДЕЛЬНО
@login_required
def reports_partners_rmg(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=4)

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            if kts_instance.tariff_per_mounth > 30:
                reagirovanie = 5000
            else:
                reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
                reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
    }

    return render(request, 'dogovornoy/reports_partners_rmg.html', context)


@login_required
def rmg_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=4, urik=False)
    rmg_fiz_count = partners_object.objects.filter(company_name_id=4, urik=False).aggregate(Count('id'))
    rmg_fiz_count = rmg_fiz_count['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        # all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            if kts_instance.tariff_per_mounth > 30:
                reagirovanie = 5000
            else:
                reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
                reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                    reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'rmg_fiz_count': rmg_fiz_count,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'rmg_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 6
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].type_object
        ws[f'D{row_num}'] = report['kts_instance'].name_object
        ws[f'E{row_num}'] = report['kts_instance'].adres
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        # ws[f'I{row_num}'] = report['kts_instance'].date_podkluchenia
        # ws[f'K{row_num}'] = report['num_days']
        ws[f'I{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        # ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'J{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'K{row_num}'] = report['itog_tehnical_services']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'L{row_num}'] = report['summ_mounth']
        ws[f'M{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'H{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    # ws[f'L{row_num}'] = report['summ_reagirovanie']
    # ws[f'M{row_num}'] = report['summ_tehnical_services']
    # ws[f'N{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'L{row_num}'] = report['itog_summ_mounth']
    # ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    # ws[f'G{row_num + 2}'] = report['rmg_fiz_count']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'E{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'E{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Сверку проверили:'
    ws[f'C{row_num + 6}'] = 'ТОО "Кузет-Сенiм"'
    ws[f'E{row_num + 6}'] = '___________________/'
    ws[f'G{row_num + 6}'] = 'Рассказчикова Н.Н./'
    ws[f'C{row_num + 7}'] = 'ТОО "RMG GROUP"'
    ws[f'E{row_num + 7}'] = '____________________/'
    ws[f'G{row_num + 7}'] = '__________________/'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO RMG Fiziki {now.date()}.xlsx'

    return response


@login_required
def rmg_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=4, urik=True)
    rmg_fiz_count = partners_object.objects.filter(company_name_id=4, urik=True).aggregate(Count('id'))
    rmg_fiz_count = rmg_fiz_count['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        # all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            if kts_instance.tariff_per_mounth > 30:
                reagirovanie = 5000
            else:
                reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
                reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                    reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'rmg_fiz_count': rmg_fiz_count,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'rmg_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 6
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].type_object
        ws[f'D{row_num}'] = report['kts_instance'].name_object
        ws[f'E{row_num}'] = report['kts_instance'].adres
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        # ws[f'I{row_num}'] = report['kts_instance'].date_podkluchenia
        # ws[f'K{row_num}'] = report['num_days']
        ws[f'I{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        # ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'J{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'K{row_num}'] = report['itog_tehnical_services']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'L{row_num}'] = report['summ_mounth']
        ws[f'M{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'H{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    # ws[f'L{row_num}'] = report['summ_reagirovanie']
    # ws[f'M{row_num}'] = report['summ_tehnical_services']
    # ws[f'N{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'L{row_num}'] = report['itog_summ_mounth']
    # ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    # ws[f'G{row_num + 2}'] = report['rmg_fiz_count']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'E{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'E{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Сверку проверили:'
    ws[f'C{row_num + 6}'] = 'ТОО "Кузет-Сенiм"'
    ws[f'E{row_num + 6}'] = '___________________/'
    ws[f'G{row_num + 6}'] = 'Рассказчикова Н.Н./'
    ws[f'C{row_num + 7}'] = 'ТОО "RMG GROUP"'
    ws[f'E{row_num + 7}'] = '____________________/'
    ws[f'G{row_num + 7}'] = '__________________/'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO RMG Fiziki {now.date()}.xlsx'

    return response


@login_required
def rmg_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=4, urik=True)
    rmg_fiz_count = partners_object.objects.filter(company_name_id=4, urik=True).aggregate(Count('id'))
    rmg_fiz_count = rmg_fiz_count['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        # all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            if kts_instance.tariff_per_mounth > 30:
                reagirovanie = 5000
            else:
                reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
                reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                    reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(
                reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.sms_number:
                itog_sms_uvedomlenie = int(
                    ((kts_instance.company_name.sms * kts_instance.sms_number) / num_days_mounth) * num_days)
            else:
                itog_sms_uvedomlenie = int((kts_instance.company_name.sms / num_days_mounth) * num_days)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'rmg_fiz_count': rmg_fiz_count,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'rmg_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 6
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].type_object
        ws[f'D{row_num}'] = report['kts_instance'].name_object
        ws[f'E{row_num}'] = report['kts_instance'].adres
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        # ws[f'I{row_num}'] = report['kts_instance'].date_podkluchenia
        # ws[f'K{row_num}'] = report['num_days']
        ws[f'I{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        # ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'J{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'K{row_num}'] = report['itog_tehnical_services']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'L{row_num}'] = report['summ_mounth']
        ws[f'M{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'H{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    # ws[f'L{row_num}'] = report['summ_reagirovanie']
    # ws[f'M{row_num}'] = report['summ_tehnical_services']
    # ws[f'N{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'L{row_num}'] = report['itog_summ_mounth']
    # ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    # ws[f'G{row_num + 2}'] = report['rmg_fiz_count']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'E{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'E{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Сверку проверили:'
    ws[f'C{row_num + 6}'] = 'ТОО "Кузет-Сенiм"'
    ws[f'E{row_num + 6}'] = '___________________/'
    ws[f'G{row_num + 6}'] = 'Рассказчикова Н.Н./'
    ws[f'C{row_num + 7}'] = 'ТОО "RMG GROUP"'
    ws[f'E{row_num + 7}'] = '____________________/'
    ws[f'G{row_num + 7}'] = '__________________/'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO RMG Uriki {now.date()}.xlsx'

    return response
# ОТЧЕТЫ АКМ КОНЕЦ








# ОТЧЕТЫ kaz-kuzet ЭКСЕЛЬ ЭКСПОРТ ПО ФИЗИКАИ И ЮРИКАМ ОТДЕЛЬНО
@login_required
def reports_partners_kazkuzet(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=3)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=3).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
    }

    return render(request, 'dogovornoy/reports_partners_kazkuzet.html', context)


@login_required
def kazkuzet_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=3, urik=False)
    kazkuzet = partners_object.objects.filter(company_name_id=3, urik=False).aggregate(Count('id'))
    kazkuzet = kazkuzet['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'kazkuzet': kazkuzet,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'kazkuzet_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        ws[f'K{row_num}'] = report['reagirovanie']
        ws[f'L{row_num}'] = report['itog_tehnical_services']
        ws[f'M{row_num}'] = report['itog_sms_uvedomlenie']
        # ws[f'P{row_num}'] = report['itog_fire_alarm']
        ws[f'N{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'D{row_num}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    ws[f'K{row_num}'] = report['summ_reagirovanie']
    ws[f'L{row_num}'] = report['summ_tehnical_services']
    ws[f'M{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'N{row_num}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    ws[f'G{row_num + 2}'] = report['kazkuzet']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'J{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'J{row_num + 5}'] = '___________________'
    ws[f'M{row_num + 5}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO KazKuzet Fiziki {now.date()}.xlsx'

    return response



@login_required
def kazkuzet_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=3, urik=True)
    kazkuzet = partners_object.objects.filter(company_name_id=3, urik=True).aggregate(Count('id'))
    kazkuzet = kazkuzet['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'kazkuzet': kazkuzet,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'kazkuzet_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        ws[f'K{row_num}'] = report['reagirovanie']
        ws[f'L{row_num}'] = report['itog_tehnical_services']
        ws[f'M{row_num}'] = report['itog_fire_alarm']
        ws[f'N{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'D{row_num}'] = 'Итого'
    ws[f'K{row_num}'] = report['summ_reagirovanie']
    ws[f'L{row_num}'] = report['summ_tehnical_services']
    ws[f'M{row_num}'] = report['summ_fire_alarm']
    ws[f'N{row_num}'] = report['summ_sms_uvedomlenie']
    ws[f'O{row_num}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 2}'] = 'Итого охраняется:'
    ws[f'G{row_num + 2}'] = report['kazkuzet']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'D{row_num + 3}'] = 'Итого к оплате за май 2024г..:'
    ws[f'J{row_num + 3}'] = report['itog_summ_mounth']
    ws[f'D{row_num + 4}'] = '(В том числе НДС 12%)'
    ws[f'D{row_num + 5}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'J{row_num + 5}'] = '___________________'
    ws[f'M{row_num + 5}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO KazKuzet Uriki {now.date()}.xlsx'

    return response

# ОТЧЕТЫ kaz-kuzet КОНЕЦ



# ОТЧЕТЫ SGS начало
@login_required
def reports_partners_sgs(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=5)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=5).aggregate(Count('id'))
    partners_kolvo_object_ur = partners_object.objects.filter(company_name_id=5, urik=True).aggregate(Count('id'))
    partners_kolvo_object_fiz = partners_object.objects.filter(company_name_id=5, urik=False).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
        'partners_kolvo_object_ur': partners_kolvo_object_ur,
        'partners_kolvo_object_fiz': partners_kolvo_object_fiz,
    }

    return render(request, 'dogovornoy/reports_partners_sgs.html', context)


@login_required
def sgs_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=5, urik=False)
    sgs = partners_object.objects.filter(company_name_id=5, urik=False).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'sgs_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        # ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'B{row_num}'] = report['kts_instance'].name_object
        ws[f'C{row_num}'] = report['kts_instance'].adres
        ws[f'D{row_num}'] = report['kts_instance'].type_object
        ws[f'E{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'I{row_num}'] = report['itog_fire_alarm']
        ws[f'J{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        # ws[f'K{row_num}'] = report['reagirovanie']
        # ws[f'L{row_num}'] = report['itog_tehnical_services']
        # ws[f'M{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'K{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'B{row_num+2}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    # ws[f'K{row_num}'] = report['summ_reagirovanie']
    # ws[f'L{row_num}'] = report['summ_tehnical_services']
    # ws[f'M{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'K{row_num+2}'] = report['itog_summ_mounth']
    ws[f'B{row_num + 3}'] = 'Итого охраняется:'
    ws[f'D{row_num + 3}'] = report['sgs']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'B{row_num + 5}'] = 'Итого к оплате за май 2024г..:'
    ws[f'F{row_num + 5}'] = report['itog_summ_mounth']
    ws[f'B{row_num + 6}'] = '(В том числе НДС 12%)'
    ws[f'B{row_num + 7}'] = 'Бухглалтер ТОО "System of Global Safety" '
    ws[f'H{row_num + 7}'] = '_________________________'
    ws[f'B{row_num + 8}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 8}'] = '___________________'
    ws[f'K{row_num + 8}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO "SGS" Fiziki {now.date()}.xlsx'

    return response


@login_required
def sgs_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=5, urik=True)
    sgs = partners_object.objects.filter(company_name_id=5, urik=True).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'sgs_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        # ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'B{row_num}'] = report['kts_instance'].name_object
        ws[f'C{row_num}'] = report['kts_instance'].adres
        ws[f'D{row_num}'] = report['kts_instance'].type_object
        ws[f'E{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'F{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'G{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'H{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'I{row_num}'] = report['itog_fire_alarm']
        ws[f'J{row_num}'] = report['num_days']
        # ws[f'H{row_num}'] = report['itog_rent_gsm']
        # ws[f'I{row_num}'] = report['itog_telemetria']
        # ws[f'J{row_num}'] = report['itog_nabludenie']
        # ws[f'K{row_num}'] = report['reagirovanie']
        # ws[f'L{row_num}'] = report['itog_tehnical_services']
        # ws[f'M{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'K{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'B{row_num+2}'] = 'Итого'
    # ws[f'I{row_num + 1}'] = report['summ_telemetria']
    # ws[f'H{row_num + 1}'] = report['summ_rent_gsm']
    # ws[f'J{row_num}'] = report['summ_tariff_per_mounth']
    # ws[f'K{row_num}'] = report['summ_reagirovanie']
    # ws[f'L{row_num}'] = report['summ_tehnical_services']
    # ws[f'M{row_num}'] = report['summ_sms_uvedomlenie']
    # ws[f'P{row_num+1}'] = report['summ_fire_alarm']
    ws[f'K{row_num+2}'] = report['itog_summ_mounth']
    ws[f'B{row_num + 3}'] = 'Итого охраняется:'
    ws[f'C{row_num + 3}'] = report['sgs']
    # ws[f'C{row_num+8}'] = 'ТОО "КузетТехноСервис"'
    # ws[f'D{row_num+9}'] = report['summ_senim']
    # ws[f'D{row_num+8}'] = report['summ_kts']
    # ws[f'C{row_num+9}'] = 'ТОО "КузетСенiм"'
    ws[f'B{row_num + 5}'] = 'Итого к оплате за май 2024г..:'
    ws[f'F{row_num + 5}'] = report['itog_summ_mounth']
    ws[f'B{row_num + 6}'] = '(В том числе НДС 12%)'
    ws[f'B{row_num + 7}'] = 'Бухглалтер ТОО "System of Global Safety" '
    ws[f'H{row_num + 7}'] = '_________________________'
    ws[f'B{row_num + 8}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 8}'] = '_________________________'
    ws[f'K{row_num + 8}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=TOO "SGS" Uriki {now.date()}.xlsx'

    return response

# ОТЧЕТЫ SGS конец




@login_required
def reports_partners_ipkim(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=6)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=6).aggregate(Count('id'))
    partners_kolvo_object_ur = partners_object.objects.filter(company_name_id=6, urik=True).aggregate(Count('id'))
    partners_kolvo_object_fiz = partners_object.objects.filter(company_name_id=6, urik=False).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
        'partners_kolvo_object_ur': partners_kolvo_object_ur,
        'partners_kolvo_object_fiz': partners_kolvo_object_fiz,
    }

    return render(request, 'dogovornoy/reports_partners_ipkim.html', context)



@login_required
def ipkim_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=6, urik=False)
    sgs = partners_object.objects.filter(company_name_id=6, urik=False).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'ipkim_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'K{row_num}'] = report['num_days']
        ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'M{row_num}'] = report['itog_rent_gsm']
        ws[f'N{row_num}'] = report['itog_tehnical_services']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+1}'] = 'Итого'
    ws[f'O{row_num+1}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 3}'] = 'Итого охраняется:'
    ws[f'D{row_num + 3}'] = report['sgs']
    ws[f'C{row_num + 4}'] = 'Итого к оплате за май 2024г..:'
    ws[f'D{row_num + 4}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 6}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 6}'] = '_________________'
    ws[f'K{row_num + 6}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "KIM" Fiziki {now.date()}.xlsx'

    return response



@login_required
def ipkim_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=6, urik=True)
    sgs = partners_object.objects.filter(company_name_id=6, urik=True).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'ipkim_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'K{row_num}'] = report['num_days']
        ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'M{row_num}'] = report['itog_rent_gsm']
        ws[f'N{row_num}'] = report['itog_tehnical_services']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+1}'] = 'Итого'
    ws[f'O{row_num+1}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 3}'] = 'Итого охраняется:'
    ws[f'D{row_num + 3}'] = report['sgs']
    ws[f'C{row_num + 4}'] = 'Итого к оплате за май 2024г..:'
    ws[f'D{row_num + 4}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 6}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 6}'] = '_________________'
    ws[f'K{row_num + 6}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "KIM" Urik {now.date()}.xlsx'

    return response


@login_required
def reports_partners_kuzets(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=7)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=7).aggregate(Count('id'))
    partners_kolvo_object_ur = partners_object.objects.filter(company_name_id=7, urik=True).aggregate(Count('id'))
    partners_kolvo_object_fiz = partners_object.objects.filter(company_name_id=7, urik=False).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
        'partners_kolvo_object_ur': partners_kolvo_object_ur,
        'partners_kolvo_object_fiz': partners_kolvo_object_fiz,
        'summ_kts': summ_kts,
        'summ_senim': summ_senim,
    }

    return render(request, 'dogovornoy/reports_partners_kuzets.html', context)



@login_required
def kuzets_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=7, urik=False)
    sgs = partners_object.objects.filter(company_name_id=7, urik=False).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'kuzets_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'F{row_num}'] = report['num_days']
        ws[f'G{row_num}'] = report['itog_rent_gsm']
        ws[f'H{row_num}'] = report['itog_nabludenie']
        ws[f'I{row_num}'] = report['reagirovanie']
        ws[f'J{row_num}'] = report['itog_tehnical_services']
        ws[f'K{row_num}'] = report['itog_telemetria']
        ws[f'L{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'M{row_num}'] = report['summ_mounth']
        ws[f'N{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+3}'] = 'Итого'
    ws[f'M{row_num+3}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 7}'] = 'Итого охраняется:'
    ws[f'F{row_num + 7}'] = report['sgs']
    ws[f'C{row_num + 8}'] = 'ТОО "КузетТехноСервис"'
    ws[f'D{row_num + 8}'] = report['summ_senim']
    ws[f'C{row_num + 9}'] = 'ТОО "КузетТехноСервис"'
    ws[f'D{row_num + 9}'] = report['summ_kts']
    ws[f'C{row_num + 10}'] = 'Итого к оплате за май 2024г..:'
    ws[f'I{row_num + 10}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 11}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 12}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num + 12}'] = '_________________'
    ws[f'E{row_num + 12}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "Kuzet-S" Fiziki {now.date()}.xlsx'

    return response



@login_required
def kuzets_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=7, urik=True)
    sgs = partners_object.objects.filter(company_name_id=7, urik=True).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services
        summ_all_company = summ_kts + summ_senim

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
            'summ_all_company': summ_all_company,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'kuzets_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        # ws[f'C{row_num}'] = report['all_object_number']
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'F{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'G{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'H{row_num}'] = report['num_days']
        ws[f'I{row_num}'] = report['itog_telemetria']
        ws[f'J{row_num}'] = report['itog_rent_gsm']
        ws[f'K{row_num}'] = report['itog_nabludenie']
        ws[f'L{row_num}'] = report['reagirovanie']
        ws[f'M{row_num}'] = report['itog_tehnical_services']
        ws[f'N{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'O{row_num}'] = report['summ_mounth']
        ws[f'P{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+4}'] = 'Итого'
    ws[f'O{row_num+4}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 7}'] = 'Итого охраняется:'
    ws[f'E{row_num + 7}'] = report['sgs']
    ws[f'C{row_num + 8}'] = 'ТОО "КузетТехноСервис"'
    ws[f'D{row_num + 8}'] = report['summ_senim']
    ws[f'C{row_num + 9}'] = 'ТОО "КузетТехноСервис"'
    ws[f'D{row_num + 9}'] = report['summ_kts']
    ws[f'C{row_num + 10}'] = 'Итого к оплате за май 2024г..:'
    # ws[f'D{row_num + 10}'] = report['summ_all_company']
    ws[f'C{row_num + 11}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 12}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num + 12}'] = '_________________'
    ws[f'E{row_num + 12}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "Kuzet-S" Uriki {now.date()}.xlsx'

    return response











@login_required
def reports_partners_samohvalov(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=8)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=8).aggregate(Count('id'))
    partners_kolvo_object_ur = partners_object.objects.filter(company_name_id=8, urik=True).aggregate(Count('id'))
    partners_kolvo_object_fiz = partners_object.objects.filter(company_name_id=8, urik=False).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        if kts_instance.primechanie == '50% на 50%':
            summ_mounth = int((itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm) / 2)
        else:
            summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm

        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
        'partners_kolvo_object_ur': partners_kolvo_object_ur,
        'partners_kolvo_object_fiz': partners_kolvo_object_fiz,
    }

    return render(request, 'dogovornoy/reports_partners_samohvalov.html', context)


@login_required
def samohvalov_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=8, urik=False)
    sgs = partners_object.objects.filter(company_name_id=8, urik=False).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        if kts_instance.primechanie == '50% на 50%':
            summ_mounth = (itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm) / 2
        else:
            summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm

        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'samohvalov_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['itog_fire_alarm']
        ws[f'K{row_num}'] = report['itog_tehnical_services']
        ws[f'L{row_num}'] = report['num_days']
        ws[f'M{row_num}'] = report['summ_mounth']
        ws[f'N{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+2}'] = 'Итого'
    ws[f'M{row_num+2}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = 'Итого охраняется:'
    ws[f'F{row_num + 5}'] = report['sgs']
    ws[f'C{row_num + 6}'] = 'Итого к оплате за май 2024г..:'
    ws[f'E{row_num + 6}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 7}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 8}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num + 8}'] = '_________________'
    ws[f'E{row_num + 8}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "Samohvalov" Fiziki {now.date()}.xlsx'

    return response



@login_required
def samohvalov_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=8, urik=True)
    sgs = partners_object.objects.filter(company_name_id=8, urik=True).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0
    itog_tehnical_services = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        if kts_instance.primechanie == '50% на 50%':
            summ_mounth = (itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm) / 2
        else:
            summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm

        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth
        summ_kts = summ_telemetria + summ_rent_gsm + summ_nabludenie + summ_sms_uvedomlenie
        summ_senim = summ_reagirovanie + summ_tehnical_services

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
            'summ_kts': summ_kts,
            'summ_senim': summ_senim,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'samohvalov_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['itog_fire_alarm']
        ws[f'K{row_num}'] = report['itog_tehnical_services']
        ws[f'L{row_num}'] = report['num_days']
        ws[f'M{row_num}'] = report['summ_mounth']
        ws[f'N{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+2}'] = 'Итого'
    ws[f'M{row_num+2}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = 'Итого охраняется:'
    ws[f'F{row_num + 5}'] = report['sgs']
    ws[f'C{row_num + 6}'] = 'Итого к оплате за май 2024г..:'
    ws[f'E{row_num + 6}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 7}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 8}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'D{row_num + 8}'] = '_________________'
    ws[f'E{row_num + 8}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "Samohvalov" uriki {now.date()}.xlsx'

    return response







@login_required
def reports_partners_sobsecutity(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=9)
    partners_kolvo_object = partners_object.objects.filter(company_name_id=9).aggregate(Count('id'))
    partners_kolvo_object_ur = partners_object.objects.filter(company_name_id=9, urik=True).aggregate(Count('id'))
    partners_kolvo_object_fiz = partners_object.objects.filter(company_name_id=9, urik=False).aggregate(Count('id'))

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
        })

    context = {
        'reports': reports,
        'start_of_month': start_of_month,
        'end_of_month': end_of_month,
        'summ_telemetria': summ_telemetria,
        'summ_rent_gsm': summ_rent_gsm,
        'summ_nabludenie': summ_nabludenie,
        'summ_reagirovanie': summ_reagirovanie,
        'summ_tehnical_services': summ_tehnical_services,
        'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
        'summ_fire_alarm': summ_fire_alarm,
        'itog_summ_mounth': itog_summ_mounth,
        'partners_kolvo_object': partners_kolvo_object,
        'partners_kolvo_object_ur': partners_kolvo_object_ur,
        'partners_kolvo_object_fiz': partners_kolvo_object_fiz,
    }

    return render(request, 'dogovornoy/reports_partners_sobsecurity.html', context)




@login_required
def sobsecutity_download_fiz(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=9, urik=False)
    sgs = partners_object.objects.filter(company_name_id=9, urik=False).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'sobsecutity_download_fiz.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['itog_rent_gsm']
        ws[f'K{row_num}'] = report['itog_fire_alarm']
        ws[f'L{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'M{row_num}'] = report['num_days']
        ws[f'N{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+1}'] = 'Итого'
    ws[f'N{row_num+1}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 3}'] = 'Итого охраняется:'
    ws[f'D{row_num + 3}'] = report['sgs']
    ws[f'C{row_num + 4}'] = 'Итого к оплате за май 2024г..:'
    ws[f'D{row_num + 4}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 6}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 6}'] = '_________________'
    ws[f'K{row_num + 6}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "KIM" Fiziki {now.date()}.xlsx'

    return response



@login_required
def sobsecutity_download_ur(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc).date()
    end_of_month = datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc).date()
    num_days_mounth = calendar.monthrange(now.year, now.month)[1]  # Default to full month days

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if start_date and end_date:
            start_of_month = parse_date(start_date)
            end_of_month = parse_date(end_date)

    partners_object_podkl = partners_object.objects.filter(company_name_id=9, urik=True)
    sgs = partners_object.objects.filter(company_name_id=9, urik=True).aggregate(Count('id'))
    sgs = sgs['id__count']

    reports = []
    summ_telemetria = 0
    summ_rent_gsm = 0
    summ_nabludenie = 0
    summ_reagirovanie = 0
    summ_tehnical_services = 0
    summ_sms_uvedomlenie = 0
    itog_summ_mounth = 0
    summ_fire_alarm = 0
    summ_tariff_per_mounth = 0

    for kts_instance in partners_object_podkl:
        tarif_nabludenia = None
        all_object_number = str(kts_instance.object_number) + "\\" + str(kts_instance.gsm_number)

        if kts_instance.date_otkluchenia:
            if isinstance(start_of_month, datetime):
                start_of_month = start_of_month.date()
            if isinstance(end_of_month, datetime):
                end_of_month = end_of_month.date()

            if (kts_instance.date_otkluchenia > start_of_month) and (kts_instance.date_podkluchenia < start_of_month):
                num_days = (kts_instance.date_otkluchenia - start_of_month).days
            elif (kts_instance.date_otkluchenia > start_of_month) and (
                    kts_instance.date_podkluchenia >= start_of_month):
                num_days = (kts_instance.date_otkluchenia - kts_instance.date_podkluchenia).days
            elif kts_instance.date_otkluchenia > start_of_month:
                num_days = num_days_mounth - (kts_instance.date_podkluchenia - kts_instance.date_otkluchenia).days
            else:
                num_days = (kts_instance.date_otkluchenia - start_of_month).days

        else:
            if kts_instance.date_podkluchenia > start_of_month:
                num_days = (end_of_month - kts_instance.date_podkluchenia).days + 1
            else:
                num_days = num_days_mounth

        if kts_instance.telemetria:
            itog_telemetria = int((kts_instance.company_name.telemetria / num_days_mounth) * num_days)
        else:
            itog_telemetria = 0

        if kts_instance.rent_gsm:
            if kts_instance.urik:
                itog_rent_gsm = int((kts_instance.company_name.arenda_ur / num_days_mounth) * num_days)
            else:
                itog_rent_gsm = int((kts_instance.company_name.arenda_fiz / num_days_mounth) * num_days)
        else:
            itog_rent_gsm = 0

        if kts_instance.nabludenie:
            if kts_instance.urik:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_ur / num_days_mounth) * num_days)
            else:
                itog_nabludenie = int((kts_instance.company_name.nabludenie_fiz / num_days_mounth) * num_days)
        else:
            itog_nabludenie = 0

        if kts_instance.tehnical_services:
            if kts_instance.urik:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_ur / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
            else:
                itog_tehnical_services = (kts_instance.company_name.tehnic_srv_cost_fiz / num_days_mounth) * num_days
                itog_tehnical_services = math.ceil(itog_tehnical_services) if itog_tehnical_services - math.floor(
                    itog_tehnical_services) > 0.5 else math.floor(
                    itog_tehnical_services)
        else:
            itog_tehnical_services = 0

        if kts_instance.fire_alarm:
            if kts_instance.urik:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_ur / num_days_mounth) * num_days)
            else:
                itog_fire_alarm = int((kts_instance.company_name.pozharka_fiz / num_days_mounth) * num_days)
        else:
            itog_fire_alarm = 0

        if kts_instance.urik:
            reagirovanie = (kts_instance.hours_mounth * kts_instance.tariff_per_mounth) / num_days_mounth * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)
        else:
            reagirovanie = (kts_instance.tariff_per_mounth / num_days_mounth) * num_days
            reagirovanie = math.ceil(reagirovanie) if reagirovanie - math.floor(reagirovanie) > 0.5 else math.floor(reagirovanie)

        if kts_instance.sms_uvedomlenie:
            if kts_instance.urik:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms_ur)
            else:
                if kts_instance.sms_number:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms * kts_instance.sms_number)
                else:
                    itog_sms_uvedomlenie = int(kts_instance.company_name.sms)
        else:
            itog_sms_uvedomlenie = 0

        summ_mounth = itog_telemetria + itog_rent_gsm + itog_nabludenie + reagirovanie + itog_tehnical_services + itog_sms_uvedomlenie + itog_fire_alarm
        summ_telemetria += itog_telemetria
        summ_rent_gsm += itog_rent_gsm
        summ_nabludenie += itog_nabludenie
        summ_reagirovanie += reagirovanie
        summ_tehnical_services += itog_tehnical_services
        summ_sms_uvedomlenie += itog_sms_uvedomlenie
        summ_fire_alarm += itog_fire_alarm
        summ_tariff_per_mounth += kts_instance.tariff_per_mounth
        itog_summ_mounth += summ_mounth

        reports.append({
            'kts_instance': kts_instance,
            'tarif_nabludenia': tarif_nabludenia,
            'num_days': num_days,
            'num_days_mounth': num_days_mounth,
            'itog_telemetria': itog_telemetria,
            'itog_rent_gsm': itog_rent_gsm,
            'itog_nabludenie': itog_nabludenie,
            'itog_tehnical_services': itog_tehnical_services,
            'itog_sms_uvedomlenie': itog_sms_uvedomlenie,
            'itog_fire_alarm': itog_fire_alarm,
            'reagirovanie': reagirovanie,
            'summ_mounth': summ_mounth,
            'summ_telemetria': summ_telemetria,
            'summ_rent_gsm': summ_rent_gsm,
            'summ_nabludenie': summ_nabludenie,
            'summ_reagirovanie': summ_reagirovanie,
            'summ_tehnical_services': summ_tehnical_services,
            'summ_sms_uvedomlenie': summ_sms_uvedomlenie,
            'summ_fire_alarm': summ_fire_alarm,
            'itog_summ_mounth': itog_summ_mounth,
            'summ_tariff_per_mounth': summ_tariff_per_mounth,
            'all_object_number': all_object_number,
            'sgs': sgs,
        })

    # Загрузка шаблона Excel и инициализация row_num
    template_path = os.path.join(settings.MEDIA_ROOT, 'sobsecutity_download_ur.xlsx')
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    # Start filling in the data from row 2 (assuming row 1 is the header)
    row_num = 10
    for report in reports:
        ws[f'A{row_num}'] = report['kts_instance'].object_number
        ws[f'B{row_num}'] = report['kts_instance'].gsm_number
        ws[f'C{row_num}'] = report['kts_instance'].name_object
        ws[f'D{row_num}'] = report['kts_instance'].adres
        ws[f'E{row_num}'] = report['kts_instance'].type_object
        ws[f'F{row_num}'] = str(report['kts_instance'].vid_sign)
        ws[f'G{row_num}'] = report['kts_instance'].hours_mounth
        ws[f'H{row_num}'] = report['kts_instance'].date_podkluchenia
        ws[f'I{row_num}'] = report['kts_instance'].tariff_per_mounth
        ws[f'J{row_num}'] = report['itog_rent_gsm']
        ws[f'K{row_num}'] = report['itog_fire_alarm']
        ws[f'L{row_num}'] = report['itog_sms_uvedomlenie']
        ws[f'M{row_num}'] = report['num_days']
        ws[f'N{row_num}'] = report['summ_mounth']
        ws[f'O{row_num}'] = report['kts_instance'].primechanie
        row_num += 1

    ws[f'C{row_num+1}'] = 'Итого'
    ws[f'N{row_num+1}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 3}'] = 'Итого охраняется:'
    ws[f'D{row_num + 3}'] = report['sgs']
    ws[f'C{row_num + 4}'] = 'Итого к оплате за май 2024г..:'
    ws[f'D{row_num + 4}'] = report['itog_summ_mounth']
    ws[f'C{row_num + 5}'] = '(В том числе НДС 12%)'
    ws[f'C{row_num + 6}'] = 'Исполнитель: гл.бухгалтер'
    ws[f'H{row_num + 6}'] = '_________________'
    ws[f'K{row_num + 6}'] = 'Рассказчикова Н.Н.'

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=ip "KIM" Urik {now.date()}.xlsx'

    return response


@login_required
def reports_kolvo(request):
    now = timezone.now()
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    end_of_month = timezone.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1], tzinfo=timezone.utc)

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

        # 2 Все объекты до выбранной даты
        kts_podkl = kts.objects.filter(company_name_id=company.id, date_podkluchenia__lte=end_of_month,
                                       date_otklulchenia = None, urik=True, exclude_from_report=False)

        # Всего на начало выбранного месяца
        kts_count_podkl = kts.objects.filter(company_name_id=company.id, urik=True, date_podkluchenia__lte=start_of_month,
                                             date_otklulchenia = None, exclude_from_report=False).aggregate(Count('id'))

        kts_fiz_podkl = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia = None,
                                           date_podkluchenia__lte=start_of_month, exclude_from_report=False).aggregate(Count('id'))

        # Всего на конец выбранного месяца
        kts_count_podkl_end = kts.objects.filter(company_name_id=company.id, date_otklulchenia = None, urik=True,
                                             date_podkluchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        kts_fiz_podkl_end = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia = None,
                                           date_podkluchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        # принято(в т.ч.после вр.снятия )
        kolvo_podkl_obj = kts.objects.filter(company_name_id=company.id, date_otklulchenia = None,
                                             date_podkluchenia__gte=start_of_month, exclude_from_report=False,
                                             date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        kolvo_podkl_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia = None,
                                             exclude_from_report=False,date_podkluchenia__lte=end_of_month).aggregate(Count('id'))

        # расторженно (в т.ч.после вр.снятия )
        kolvo_otkl_obj = kts.objects.filter(company_name_id=company.id, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        kolvo_otkl_fiz = kts.objects.filter(company_name_id=company.id, urik=False, date_otklulchenia__gte=start_of_month,
                                            date_otklulchenia__lte=end_of_month, exclude_from_report=False).aggregate(Count('id'))

        # экипажи физические лица
        gruppa_reagirovania_911_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia = None,
                                                    urik=False, gruppa_reagirovania='911', exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_bravo21_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                     urik=False, gruppa_reagirovania='Браво-21', exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_sms_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        urik=False, gruppa_reagirovania='СМС', exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_asker_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=False, gruppa_reagirovania='Эскер', exclude_from_report=False).aggregate(Count('id'))

        gruppa_reagirovania_zardem_fiz = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=False, gruppa_reagirovania='Жардем', exclude_from_report=False).aggregate(Count('id'))

        # экипажи юридические лица
        gruppa_reagirovania_911_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=True, gruppa_reagirovania='911').aggregate(Count('id'))

        gruppa_reagirovania_bravo21_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                    urik=True, gruppa_reagirovania='Браво-21').aggregate(Count('id'))

        gruppa_reagirovania_sms_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                         urik=True, gruppa_reagirovania='СМС').aggregate(Count('id'))

        gruppa_reagirovania_asker_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        urik=True, gruppa_reagirovania='Эскер').aggregate(Count('id'))

        gruppa_reagirovania_zardem_ur = kts.objects.filter(company_name_id=company.id, date_otklulchenia=None,
                                                        urik=True, gruppa_reagirovania='Жардем').aggregate(Count('id'))

        reports.append({
            'companies': companies,
            'urik_companies': urik_companies,
            'non_urik_companies_quantity': non_urik_companies_quantity,
            'kts_podkl': kts_podkl,
            'kts_count_podkl': kts_count_podkl,
            'kts_fiz_podkl': kts_fiz_podkl,
            'kts_count_podkl_end': kts_count_podkl_end,
            'kts_fiz_podkl_end': kts_fiz_podkl_end,
            'start_of_month': start_of_month,
            'end_of_month': end_of_month,
            'end_of_month': end_of_month,
            'kolvo_podkl_obj': kolvo_podkl_obj,
            'kolvo_podkl_fiz': kolvo_podkl_fiz,
            'kolvo_otkl_obj': kolvo_otkl_obj,
            'kolvo_otkl_fiz': kolvo_otkl_fiz,
            'gruppa_reagirovania_911_fiz': gruppa_reagirovania_911_fiz,
            'gruppa_reagirovania_sms_fiz': gruppa_reagirovania_sms_fiz,
            'gruppa_reagirovania_asker_fiz': gruppa_reagirovania_asker_fiz,
            'gruppa_reagirovania_zardem_fiz': gruppa_reagirovania_zardem_fiz,
            'gruppa_reagirovania_bravo21_fiz': gruppa_reagirovania_bravo21_fiz,
            'gruppa_reagirovania_911_ur': gruppa_reagirovania_911_ur,
            'gruppa_reagirovania_sms_ur': gruppa_reagirovania_sms_ur,
            'gruppa_reagirovania_asker_ur': gruppa_reagirovania_asker_ur,
            'gruppa_reagirovania_zardem_ur': gruppa_reagirovania_zardem_ur,
            'gruppa_reagirovania_bravo21_ur': gruppa_reagirovania_bravo21_ur,
        })
        context = {'reports': reports, 'start_of_month': start_of_month, 'end_of_month': end_of_month}
    return render(request, 'dogovornoy/reports_kolvo.html', context)
