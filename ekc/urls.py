from django.urls import path
from .views import *

urlpatterns = [
    path('guardedobject/<int:pk>/', GuardedObjectDetailView.as_view(), name='guardedobject_detail'),
    path('ekcbaza/', EkcBaza.as_view(), name='ekcbaza'),
    path('reports/technician/', reports_technician, name='reports_technician'),
    path('reports/reports_crew/', reports_crew, name='reports_crew'),
    path('reports/export_crew_to_excel/', export_crew_to_excel, name='export_crew_to_excel'),
    path('generate_word/<int:object_id>/', generate_word, name='generate_word'),
]
