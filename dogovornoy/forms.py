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
                format=('%d-%m-%Y'),
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
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'date_otklulchenia': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'gruppa_reagirovania': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'vid_rpo': forms.Textarea(attrs={'class': 'form-control'}),
            'primechanie': forms.Textarea(attrs={'class': 'form-control'}),
            'agentskie': forms.TextInput(attrs={'class': 'form-control'}),
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_registration': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')


class AdditionalServiceForm(forms.ModelForm):
    class Meta:
        model = AdditionalService
        fields = ['service_name', 'price', 'date_added', 'date_unsubscribe']
        exclude = ['kts']
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'date_added': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'date_unsubscribe': forms.DateInput(
                format=('%d-%m-%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


