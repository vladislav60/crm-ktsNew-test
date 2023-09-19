from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget


from .models import *


# Форма добавления нового клиента в договорной связанные с моделями
class AddKlientDogForm(forms.ModelForm):
    class Meta:
        model = kts
        fields = ['udv_number', 'date_udv', 'company_name', 'dogovor_number', 'data_zakluchenia', 'nalichiye_dogovora',
                  'mat_otv', 'act_ty', 'time_reag', 'time_reag_nebol', 'yslovie_dogovora', 'klient_name', 'name_object', 'adres', 'iin_bin', 'telephone',
                  'vid_sign', 'urik', 'chasi_po_dog', 'dop_uslugi', 'abon_plata', 'itog_oplata',
                  'object_number', 'peredatchik_number', 'stoimost_rpo', 'date_podkluchenia', 'date_otklulchenia',
                  'gruppa_reagirovania', 'email',
                  'vid_rpo', 'primechanie', 'agentskie', 'photo']
        widgets = {
            'udv_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_udv': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'urik': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dogovor_number': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'data_zakluchenia': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'required': 'True', 'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'nalichiye_dogovora': forms.TextInput(attrs={'class': 'form-control'}),
            'mat_otv': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'act_ty': forms.TextInput(attrs={'class': 'form-control'}),
            'time_reag': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'time_reag_nebol': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'yslovie_dogovora': forms.TextInput(attrs={'class': 'form-control'}),
            'klient_name': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'name_object': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'adres': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'iin_bin': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'vid_sign': forms.Select(attrs={'class': 'form-select'}),
            'chasi_po_dog': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'dop_uslugi': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'abon_plata': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'itog_oplata': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'object_number': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'peredatchik_number': forms.TextInput(attrs={'class': 'form-control'}),
            'stoimost_rpo': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'date_podkluchenia': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'date_otklulchenia': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'gruppa_reagirovania': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'vid_rpo': forms.Textarea(attrs={'class': 'form-control'}),
            'primechanie': forms.Textarea(attrs={'class': 'form-control'}),
            'agentskie': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # company_name = forms.CharField(max_length=100, label='Наименование компании*')
    # dogovor_number = forms.CharField(max_length=40, label='Номер договора*')
    # data_zakluchenia = forms.DateField(label="Дата заключения*")
    # nalichiye_dogovora = forms.CharField(label="Наличие Договора", required='False')
    # mat_otv = forms.IntegerField(label="Мат.отв*")
    # act_ty = forms.CharField(max_length=200, label="Акты ТУ", required='False')
    # time_reag = forms.IntegerField(label="Время реагирования*")
    # yslovie_dogovora = forms.CharField(max_length=100, label="Условия договора", required='False')
    # klient_name = forms.CharField(max_length=255, label="Наименование Клиента*")
    # name_object = forms.CharField(max_length=255, label="Наименование объекта*")
    # adres = forms.CharField(max_length=255, label="Адрес объекта*")
    # iin_bin = forms.IntegerField(label="ИИН/БИН*")
    # telephone = forms.CharField(max_length=255, label="Телефон*")
    # vid_sign = forms.CharField(max_length=40, label="Вид сигнализации*")
    # urik = forms.BooleanField(label="ЮЛ*", initial='False')
    # chasi_po_dog = forms.IntegerField(label="Часы по договору*")
    # dop_uslugi = forms.IntegerField(label="Доп.услуги", required='False')
    # abon_plata = forms.IntegerField(label="Абон.плата*")
    # itog_oplata = forms.IntegerField(label="Итого", required='False')
    # tehnik_obsluga = forms.IntegerField(label="Тех.обсуживание", required='False')
    # object_number = forms.IntegerField(label="№ объекта", required='False')
    # peredatchik_number = forms.CharField(label="№ передатчика/GSM", required='False')
    # stoimost_rpo = forms.IntegerField(label="Стоимость РПО*")
    # date_podkluchenia = forms.DateField(label="Дата подключения", required='False')
    # date_otklulchenia = forms.DateField(label="Дата отключения", required='False')
    # gruppa_reagirovania = forms.CharField(max_length=50, label="Группа реагирования", required='False')
    # email = forms.CharField(max_length=100, label="Электронный адрес", required='False')
    # primechanie = forms.CharField(label="Примечание", widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), required='False')
    # agentskie = forms.CharField(max_length=255, label="Агентские", required='False')

    # def clean_title(self):
    #     klient_name = self.cleaned_data['klient_name']
    #     if len(klient_name) > 200:
    #         raise ValidationError('Длина превышает 200 символов')
    #
    #     return klient_name


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')


