from django import forms
from django.contrib.auth.models import User
from dogovornoy.models import *  # Импорт модели TaskReason из приложения dogovornoy
from pult.models import *

class TaskCreationForm(forms.ModelForm):
    technician = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__department='Техники'),
        label="Выберите техника",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    reason = forms.ModelChoiceField(
        queryset=TaskReason.objects.all(),
        label="Причина задачи",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    note = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Примечание"
    )

    class Meta:
        model = TechnicalTask
        fields = ['technician', 'reason', 'note']
