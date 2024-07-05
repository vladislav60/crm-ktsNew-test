from django.urls import path
from . import views

urlpatterns = [
    path('cards/', views.card_list, name='card_list'),
]
