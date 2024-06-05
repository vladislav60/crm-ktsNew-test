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
    # Ссылка на страницу базы договорного партнеров
    path('baza_partnerov/', views.DogBazaPartners.as_view(), name='baza_partnerov'),
    # Ссылка на страницу реквизитов
    path('rekvizity/', views.Rekvizity.as_view(), name='rekvizity'),
    # Ссылка на страницу реквизитов
    path('partners_rekvizity/', views.RekvizityPartners.as_view(), name='partners_rekvizity'),
    # Ссылка на страницу импорта объектов
    path('importexel/', importexcel, name='importexel'),
    # Ссылка на страницу импорта объектов партнеров
    path('partnerts_importexel/', partnerts_importexel, name='partnerts_importexel'),
    # Ссылка на страницу импорта реквизитов
    path('importrekvizity/', importrekvizity, name='importrekvizity'),
    # Ссылка на страницу импорта видов сигнализации
    path('importvidsign/', importvidsign, name='importvidsign'),
    # Ссылка на страницу импорта экипажей
    path('importekipazh/', importekipazh, name='importekipazh'),
    # Ссылка на страницу Новый клиент
    path('add_client/', views.AddClient.as_view(), name='add_client'),
    # Ссылка на страницу Новый клиент партнеров
    path('add_client_partner/', views.AddClientPartner.as_view(), name='add_client_partner'),
    # Ссылка на страницу Отчеты договорной
    path('reports_dog/', reports, name='reports_dog'),
    # Ссылка на страницу Отчеты агенские
    path('reports_agentskie/', reports_agentskie, name='reports_agentskie'),
    # Ссылка на страницу Отчеты партнеры
    path('reports_partners/', reports_partners, name='reports_partners'),
    # Ссылка на страницу Отчеты партнеры АКМ
    path('reports_partners_akm/', reports_partners_akm, name='reports_partners_akm'),
    # Ссылка на страницу экпорь Эксель физики АКМ
    path('akm_download_fiz/', akm_download_fiz, name='akm_download_fiz'),
    # Ссылка на страницу экпорь Эксель юрики АКМ
    path('akm_download_ur/', akm_download_ur, name='akm_download_ur'),
    # Ссылка на страницу Отчеты партнеры RMG
    path('reports_partners_rmg/', reports_partners_rmg, name='reports_partners_rmg'),
    # Ссылка на страницу экпорь Эксель физики RMG
    path('rmg_download_fiz/', rmg_download_fiz, name='rmg_download_fiz'),
    # Ссылка на страницу экпорь Эксель юрики RMG
    path('rmg_download_ur/', rmg_download_ur, name='rmg_download_ur'),
    # Ссылка на страницу Отчеты партнеры Kaz-Kuzet
    path('reports_partners_kazkuzet/', reports_partners_kazkuzet, name='reports_partners_kazkuzet'),
    # Ссылка на страницу экпорь Эксель физики Kaz-Kuzet
    path('kazkuzet_download_fiz/', kazkuzet_download_fiz, name='kazkuzet_download_fiz'),
    # Ссылка на страницу экпорь Эксель юрики Kaz-Kuzet
    path('kazkuzet_download_ur/', kazkuzet_download_ur, name='kazkuzet_download_ur'),
    # Ссылка на кнопку скачать Отчеты партнеры юрики СГС-Плюс
    path('reports_partners_download_urik/', reports_partners_download_urik, name='reports_partners_download_urik'),
    # Ссылка на кнопку скачать Отчеты партнеры fizik СГС-Плюс
    path('sgs_plus_download_fiz/', sgs_plus_download_fiz, name='sgs_plus_download_fiz'),
    # Ссылка на кнопку скачать Отчеты партнеры fizik СГС
    path('reports_partners_sgs/', reports_partners_sgs, name='reports_partners_sgs'),
    path('sgs_download_fiz/', sgs_download_fiz, name='sgs_download_fiz'),
    path('sgs_download_ur/', sgs_download_ur, name='sgs_download_ur'),
    # Ссылка страницу отчета ИП "Ким"
    path('reports_partners_ipkim/', reports_partners_ipkim, name='reports_partners_ipkim'),
    path('ipkim_download_fiz/', ipkim_download_fiz, name='ipkim_download_fiz'),
    path('ipkim_download_ur/', ipkim_download_ur, name='ipkim_download_ur'),
    # Ссылка страницу отчета ИП "Кузет-С"
    path('reports_partners_kuzets/', reports_partners_kuzets, name='reports_partners_kuzets'),
    path('kuzets_download_fiz/', kuzets_download_fiz, name='kuzets_download_fiz'),
    path('kuzets_download_ur/', kuzets_download_ur, name='kuzets_download_ur'),
    # Ссылка страницу отчета ИП "Самохвалов"
    path('reports_partners_samohvalov/', reports_partners_samohvalov, name='reports_partners_samohvalov'),
    path('samohvalov_download_fiz/', samohvalov_download_fiz, name='samohvalov_download_fiz'),
    path('samohvalov_download_ur/', samohvalov_download_ur, name='samohvalov_download_ur'),
    # Ссылка страницу отчета ИП "Самохвалов"
    path('reports_partners_sobsecutity/', reports_partners_sobsecutity, name='reports_partners_sobsecutity'),
    path('sobsecutity_download_fiz/', sobsecutity_download_fiz, name='sobsecutity_download_fiz'),
    path('sobsecutity_download_ur/', sobsecutity_download_ur, name='sobsecutity_download_ur'),
    # Ссылка на страницу Отчеты кол-во объектов
    path('reports_kolvo/', reports_kolvo, name='reports_kolvo'),
    # Ссылка на страницу изменения клиента
    path('update_client/<int:klient_id>/', views.update_client, name='update_client'),
    # Ссылка на страницу изменения клиента партнеров
    path('update_client_partner/<int:partner_klient_id>/', views.update_client_partner, name='update_client_partner'),
    # Ссылка на страницу удалить клиента
    path('delete_client/<int:klient_id>/', views.delete_client, name='delete_client'),
    # Ссылка на страницу удалить клиента партнеров
    path('delete_client_partners/<int:partner_klient_id>/', views.delete_client_partners, name='delete_client_partners'),
    # Ссылка на страницу Создать договор
    path('create_dogovor/<int:klient_id>/', create_dogovor, name='create_dogovor'),
    # Ссылка на страницу Карточка клиента
    path('kartochka_klienta/<int:klient_id>/', views.KartochkaKlienta.as_view(), name='kartochka_klienta'),
    # Ссылка на страницу Карточка клиента
    path('kartochka_partner/<int:partner_klient_id>/', views.KartochkaPartner.as_view(), name='kartochka_partner'),
    # path('search/', search_kts, name='search_kts'),
    path('additional_service/<int:service_id>', views.delete_additional_service, name='delete_additional_service'),
    # Функция редактирования дополнительный услуг
    path('additional_service/<int:service_id>/edit/', views.edit_additional_service, name='edit_additional_service'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

