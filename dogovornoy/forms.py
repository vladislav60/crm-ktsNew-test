from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.utils.timezone import now


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
                  'vid_rpo', 'primechanie', 'prochee', 'agentskie', 'photo', 'exclude_from_report', 'iik', 'bik', 'bank', 'rezhim_raboti', 'fio_direktor_sokr',
                  'fio_direktor_polnoe',  'dolznost', 'ucereditel_doc', 'urik_adress']
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
                attrs={'min': '0', 'class': 'form-control', 'max': '10000000000'}),
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
            'iik': forms.TextInput(attrs={'class': 'form-control'}),
            'bik': forms.TextInput(attrs={'class': 'form-control'}),
            'bank': forms.TextInput(attrs={'class': 'form-control'}),
            'rezhim_raboti': forms.TextInput(attrs={'class': 'form-control'}),
            'fio_direktor_sokr': forms.TextInput(attrs={'class': 'form-control'}),
            'fio_direktor_polnoe': forms.TextInput(attrs={'class': 'form-control'}),
            'dolznost': forms.TextInput(attrs={'class': 'form-control'}),
            'ucereditel_doc': forms.TextInput(attrs={'class': 'form-control'}),
            'urik_adress': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddKlientDogFormPartner(forms.ModelForm):
    class Meta:
        model = partners_object
        fields = [
            'object_number', 'gsm_number', 'name_object', 'adres', 'type_object', 'vid_sign', 'hours_mounth',
            'date_podkluchenia', 'tariff_per_mounth', 'tehnical_services', 'rent_gsm', 'fire_alarm', 'telemetria',
            'nabludenie', 'sms_uvedomlenie', 'sms_number', 'kolvo_day', 'primechanie', 'ekipazh', 'urik', 'company_name',
            'date_otkluchenia', 'prochee']
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
            'tariff_per_mounth': forms.NumberInput(attrs={'class': 'form-control'}),
            'sms_uvedomlenie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sms_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'tehnical_services': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rent_gsm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fire_alarm': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'telemetria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nabludenie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kolvo_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'primechanie': forms.Textarea(attrs={'class': 'form-control'}),
            'ekipazh': forms.Select(attrs={'class': 'form-control'}),
            'urik': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_otkluchenia': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'prochee': forms.Textarea(attrs={'class': 'form-control'}),
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
    class Meta:
        model = Task
        fields = ['assigned_to', 'description']
        labels = {
            'client': 'Номер объекта клиента',
        }
        widgets = {
            'assigned_to': forms.Select(attrs={'data-placeholder': 'Выберите сотрудника', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class TaskFormDog(forms.ModelForm):
    client_id = forms.CharField(widget=forms.HiddenInput())  # Скрытое поле для client_id

    class Meta:
        model = Task
        fields = ['assigned_to', 'description', 'client_id']  # Добавляем поле client_id
        labels = {
            'assigned_to': 'Отправить сотруднику',
            'description': 'Описание задачи',
        }
        widgets = {
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskFormDog, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.all()  # Настройка пользователей



class TechnicalTaskFilterForm(forms.Form):
    client_object_id = forms.CharField(required=False, label='ID клиента')
    technician = forms.ModelChoiceField(queryset=User.objects.filter(userprofile__department="Техник"), required=False, label='Техник')
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False, label='Дата от')
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False, label='Дата до')



class SkaldGSMForm(forms.ModelForm):
    technik = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__department="Техник"),
        required=False,
        label='Техник',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super(SkaldGSMForm, self).__init__(*args, **kwargs)
        # Используем label_from_instance для кастомизации отображения пользователей
        self.fields['technik'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name} ({obj.username})"

    class Meta:
        model = SkaldGSM2
        fields = [
            'date_vidachi',
            'nubmer_gsm',
            'type_gsm',
            'technik',
            'podpis',
            'adres_object',
            'date_back_gsm',
            'return_reason',
        ]
        widgets = {
            'date_vidachi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_back_gsm': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nubmer_gsm': forms.NumberInput(attrs={'min': '0', 'class': 'form-control', 'max': '10000000'}),
            'type_gsm': forms.Select(attrs={'class': 'form-control'}),
            'adres_object': forms.TextInput(attrs={'class': 'form-control'}),
            'podpis': forms.TextInput(attrs={'class': 'form-control'}),
            'return_reason': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'date_vidachi': 'Дата выдачи',
            'nubmer_gsm': '№ GSM',
            'type_gsm': 'Тип GSM',
            'technik': 'Техник принявший',
            'podpis': 'Номер объекта',
            'adres_object': 'Адрес объекта',
            'return_reason': 'Причина возврата',
            'date_back_gsm': 'Дата возврата',
        }


class DateBackGSMForm(forms.ModelForm):
    date_back_gsm = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Дата возврата',
        initial=now().date()  # Устанавливаем сегодняшнюю дату
    )
    return_reason = forms.ModelChoiceField(
        queryset=ReturnReason.objects.all(),
        required=False,  # Сделайте обязательным, если это нужно
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Причина возврата'
    )

    class Meta:
        model = SkaldGSM2
        fields = ['date_back_gsm', 'return_reason']


class TechnicalTaskForm(forms.ModelForm):
    class Meta:
        model = TechnicalTask
        fields = ['arrival_time', 'completion_time', 'result']  # Замените на нужные поля
        widgets = {
            'completion_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',  # Для использования стилей Bootstrap
                },
                format='%Y-%m-%dT%H:%M',  # Формат для HTML5 input
            ),
            'arrival_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',  # Для использования стилей Bootstrap
                },
                format='%Y-%m-%dT%H:%M',  # Формат для HTML5 input
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-классы ко всем полям
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ArchTechnicalTaskForm(forms.ModelForm):
    class Meta:
        model = TechnicalTask
        fields = ['result']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'email', 'source', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }





