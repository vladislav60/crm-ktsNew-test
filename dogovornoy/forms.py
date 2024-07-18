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
                  'vid_sign', 'urik', 'chasi_po_dog', 'dop_uslugi', 'abon_plata',
                  'object_number', 'peredatchik_number', 'stoimost_rpo', 'date_podkluchenia', 'date_otklulchenia',
                  'gruppa_reagirovania', 'email', 'date_izmenenia',
                  'vid_rpo', 'primechanie', 'prochee', 'agentskie', 'photo', 'exclude_from_report']
        widgets = {
            'udv_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_udv': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'urik': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dogovor_number': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'data_zakluchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
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
                attrs={'required': 'True', 'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'required': 'True', 'class': 'form-control'}),
            'vid_sign': forms.Select(attrs={'class': 'form-select'}),
            'chasi_po_dog': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'dop_uslugi': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'abon_plata': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'object_number': forms.NumberInput(
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'peredatchik_number': forms.TextInput(attrs={'class': 'form-control'}),
            'stoimost_rpo': forms.NumberInput(
                attrs={'required': 'True', 'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'date_podkluchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'date_otklulchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'date_izmenenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'gruppa_reagirovania': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'vid_rpo': forms.Textarea(attrs={'class': 'form-control'}),
            'primechanie': forms.Textarea(attrs={'class': 'form-control'}),
            'prochee': forms.TextInput(attrs={'class': 'form-control'}),
            'agentskie': forms.TextInput(attrs={'class': 'form-control'}),
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'exclude_from_report': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AddKlientDogFormPartner(forms.ModelForm):
    class Meta:
        model = partners_object
        fields = [
            'object_number', 'gsm_number', 'name_object', 'adres', 'type_object', 'vid_sign', 'hours_mounth',
            'date_podkluchenia', 'date_otkluchenia', 'tariff_per_mounth', 'tehnical_services', 'rent_gsm', 'fire_alarm', 'telemetria',
            'nabludenie', 'sms_uvedomlenie', 'kolvo_day', 'primechanie', 'ekipazh', 'urik', 'company_name', 'sms_number',
        ]
        widgets = {
            'company_name': forms.Select(attrs={'class': 'form-control'}),
            'object_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gsm_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name_object': forms.TextInput(attrs={'class': 'form-control'}),
            'adres': forms.TextInput(attrs={'class': 'form-control'}),
            'type_object': forms.TextInput(attrs={'class': 'form-control'}),
            'vid_sign': forms.Select(attrs={'class': 'form-select'}),
            'hours_mounth': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_podkluchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'date_otkluchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'tariff_per_mounth': forms.NumberInput(attrs={'class': 'form-control'}),
            'sms_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'tehnical_services': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rent_gsm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fire_alarm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telemetria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nabludenie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_uvedomlenie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kolvo_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'primechanie': forms.Textarea(attrs={'class': 'form-control'}),
            'ekipazh': forms.Select(attrs={'class': 'form-control'}),
            'urik': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')

class PartnersImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')

class RekvizityImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')


class VidSignImportForm(forms.Form):
    excel_file = forms.FileField(label='Загрузите Excel файл')

class EkipazhImportForm(forms.Form):
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
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            'date_unsubscribe': forms.DateInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class TaskForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=kts.objects.all(),
        label="Client",
        # Указываем функцию, которая будет формировать отображаемое значение в списке
        to_field_name="name_object",  # Убедитесь, что у модели kts есть поле name_object
        empty_label="Select Client",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['client', 'assigned_to', 'description']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['client'].label_from_instance = self.label_from_instance

    # В этой функции определяем, как будет отображаться каждый элемент в списке
    def label_from_instance(self, obj):
        # Возвращаем нужное отображение, например, номер объекта или что-то еще
        return f"{str(obj.object_number) + ' - ' + str(obj.dogovor_number) + ' - ' + obj.klient_name}"



