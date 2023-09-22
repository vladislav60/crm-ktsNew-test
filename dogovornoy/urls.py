# №5 Создаём файл urls.py в приложении dogovornoy в него пишу
from django.template.context_processors import static
from django.urls import path, include, re_path
# Импорт всех пердставлений приложения
from ktscrm import settings
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Ссылка на главную страницу
    path('', index, name='home'),
    # Ссылка на страницу логина
    path('login/', login_view, name='login'),
    # Ссылка на функцию выхода
    path('logout_view', logout_view, name='logout'),
    # Ссылка на страницу базы договорного
    path('baza_dogovorov/', views.DogBaza.as_view(), name='baza_dogovorov'),
    # Ссылка на страницу реквизитов
    path('rekvizity/', views.Rekvizity.as_view(), name='rekvizity'),
    # Ссылка на страницу импорта объектов
    path('importexel/', importexcel, name='importexel'),
    # Ссылка на страницу Новый клиент
    # path('add_client/', add_client, name='add_client'),
    path('add_client/', views.AddClient.as_view(), name='add_client'),
    # Ссылка на страницу Отчеты договорной
    path('reports_dog/', reports, name='reports_dog'),
    # Ссылка на страницу Отчеты агенские
    path('reports_agentskie/', reports_agentskie, name='reports_agentskie'),
    # Ссылка на страницу изменения клиента
    path('update_client/<int:klient_id>/', views.update_client, name='update_client'),
    # Ссылка на страницу удалить клиента
    path('delete_client/<int:klient_id>/', views.delete_client, name='delete_client'),
    # Ссылка на страницу Создать договор
    path('create_dogovor/<int:klient_id>/', create_dogovor, name='create_dogovor'),
    # Ссылка на страницу Карточка клиента
    path('kartochka_klienta/<int:klient_id>/', views.KartochkaKlienta.as_view(), name='kartochka_klienta'),
    # path('search/', search_kts, name='search_kts'),
    path('additional_service/<int:service_id>', views.delete_additional_service, name='delete_additional_service'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

