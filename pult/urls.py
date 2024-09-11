from django.urls import path, include
from . import views
from .views import *
from django.contrib import admin

urlpatterns = [
    path('cards/', views.card_list, name='card_list'),
    path('alarm_report/', views.alarm_report, name='alarm_report'),
    path('alarm_report_tech/', views.alarm_report_tech, name='alarm_report_tech'),
    path('export-alarms/', export_alarms_to_excel, name='export_alarms_to_excel'),
    path('cards/<int:pk>/', card_detail, name='card_detail'),
]
