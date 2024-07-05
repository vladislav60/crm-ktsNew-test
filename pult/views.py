# pult/views.py
from django.shortcuts import render
from .models import Cards

def card_list(request):
    cards = Cards.objects.using('third_db').all()
    return render(request, 'card_list.html', {'cards': cards})
