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
    path('export_reports_to_excel/', export_reports_to_excel, name='export_reports_to_excel'),
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
    # Ссылка страницу отчета ИП "Eye Watch"
    path('reports_partners_eyewatch/', reports_partners_eyewatch, name='reports_partners_eyewatch'),
    path('eyewatch_download_fiz/', eyewatch_download_fiz, name='eyewatch_download_fiz'),
    path('eyewatch_download_ur/', eyewatch_download_ur, name='eyewatch_download_ur'),
    # Ссылка страницу отчета ТОО "Eurasian Security System"
    path('reports_partners_eurasian/', reports_partners_eurasian, name='reports_partners_eurasian'),
    path('eurasian_download_fiz/', eurasian_download_fiz, name='eurasian_download_fiz'),
    path('eurasian_download_ur/', eurasian_download_ur, name='eurasian_download_ur'),
    # Ссылка страницу отчета TOO "IVISCOM"
    path('reports_partners_iviscom/', reports_partners_iviscom, name='reports_partners_iviscom'),
    path('iviscom_download_fiz/', iviscom_download_fiz, name='iviscom_download_fiz'),
    path('iviscom_download_ur/', iviscom_download_ur, name='iviscom_download_ur'),
    # Ссылка страницу отчета ТОО "Б.М.kz Security"
    path('reports_partners_bmkz/', reports_partners_bmkz, name='reports_partners_bmkz'),
    path('bmkz_download_fiz/', bmkz_download_fiz, name='bmkz_download_fiz'),
    path('bmkz_download_ur/', bmkz_download_ur, name='bmkz_download_ur'),
    # Ссылка страницу отчета ТОО "Монолит Секьюрити"
    path('reports_partners_monolit/', reports_partners_monolit, name='reports_partners_monolit'),
    path('monolit_download_fiz/', monolit_download_fiz, name='monolit_download_fiz'),
    path('monolit_download_ur/', monolit_download_ur, name='monolit_download_ur'),
    # Ссылка страницу отчета ТОО "Tech-Mart"
    path('reports_partners_techmart/', reports_partners_techmart, name='reports_partners_techmart'),
    path('techmart_download_fiz/', techmart_download_fiz, name='techmart_download_fiz'),
    path('techmart_download_ur/', techmart_download_ur, name='techmart_download_ur'),
    # Ссылка страницу отчета ТОО "Tech-Mart"
    path('reports_partners_twojoy/', reports_partners_twojoy, name='reports_partners_twojoy'),
    path('twojoy_download_fiz/', twojoy_download_fiz, name='twojoy_download_fiz'),
    path('twojoy_download_ur/', twojoy_download_ur, name='twojoy_download_ur'),
    # Ссылка страницу отчета 	ТОО "MEDIN"
    path('reports_partners_medin/', reports_partners_medin, name='reports_partners_medin'),
    path('medin_download_fiz/', medin_download_fiz, name='medin_download_fiz'),
    path('medin_download_ur/', medin_download_ur, name='medin_download_ur'),
    # Ссылка страницу отчета   ИП "Жакитов"
    path('reports_partners_zhakitov/', reports_partners_zhakitov, name='reports_partners_zhakitov'),
    path('zhakitov_download_fiz/', zhakitov_download_fiz, name='zhakitov_download_fiz'),
    path('zhakitov_download_ur/', zhakitov_download_ur, name='zhakitov_download_ur'),
    # Ссылка страницу отчета   ТОО "Alash Group Kuzet"
    path('reports_partners_alash/', reports_partners_alash, name='reports_partners_alash'),
    path('alash_download_fiz/', alash_download_fiz, name='alash_download_fiz'),
    path('alash_download_ur/', alash_download_ur, name='alash_download_ur'),
    # Ссылка страницу отчета ТОО "Эгида-Дружина
    path('reports_partners_egida/', reports_partners_egida, name='reports_partners_egida'),
    path('egida_download_fiz/', egida_download_fiz, name='egida_download_fiz'),
    path('egida_download_ur/', egida_download_ur, name='egida_download_ur'),
    # Ссылка страницу отчета ТОО "kazvision"
    path('reports_partners_kazvision/', reports_partners_kazvision, name='reports_partners_kazvision'),
    path('kazvision_download_fiz/', kazvision_download_fiz, name='kazvision_download_fiz'),
    path('kazvision_download_ur/', kazvision_download_ur, name='kazvision_download_ur'),
    # Ссылка страницу отчета ТОО "kuzetmonitoring"
    path('reports_partners_kuzetmonitoring/', reports_partners_kuzetmonitoring, name='reports_partners_kuzetmonitoring'),
    path('kuzetmonitoring_download_fiz/', kuzetmonitoring_download_fiz, name='kuzetmonitoring_download_fiz'),
    path('kuzetmonitoring_download_ur/', kuzetmonitoring_download_ur, name='kuzetmonitoring_download_ur'),
    # Ссылка страницу отчета ТОО "securityplus"
    path('reports_partners_securityplus/', reports_partners_securityplus, name='reports_partners_securityplus'),
    path('securityplus_download_fiz/', securityplus_download_fiz, name='securityplus_download_fiz'),
    path('securityplus_download_ur/', securityplus_download_ur, name='securityplus_download_ur'),
    # Ссылка на страницу Отчеты кол-во объектов
    path('reports_kolvo/', reports_kolvo, name='reports_kolvo'),
    path('partner_reports_kolvo/', partner_reports_kolvo, name='partner_reports_kolvo'),
    path('kts_reports_kolvo/', kts_reports_kolvo, name='kts_reports_kolvo'),
    path('kolvo_hours_security/', kolvo_hours_security, name='kolvo_hours_security'),
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
    # отправка заявок
    path('create_task/', CreateTaskView.as_view(), name='create_task'),
    # path('new_task/', views.create_task, name='create_task'),
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('task/accept/<int:pk>/', AcceptTaskView.as_view(), name='accept_task'),
    path('task/complete/<int:pk>/', CompleteTaskView.as_view(), name='complete_task'),
    path('copy_client/<int:pk>/', CopyClientView.as_view(), name='copy_client'),
    path('copy_client_partner/<int:pk>/', CopyClientViewPartner.as_view(), name='copy_client_partner'),
    path('create_technical_task/', CreateTechnicalTaskView.as_view(), name='create_technical_task'),
    path('api_technicians/', TechniciansAPIView, name='api_technicians'),
    path('api_task_reasons/', TaskReasonsAPIView, name='api_task_reasons'),
    path('telegram_webhook/', telegram_webhook, name='telegram_webhook'),
    path('technical_task_list/', TechnicalTaskListView.as_view(), name='technical_task_list'),
    path('tasks/<int:pk>/edit/', views.TechnicalTaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TechnicalTaskDeleteView.as_view(), name='task_delete'),
    path('archive_technical_task_list/', ArchiveTechnicalTaskListView.as_view(), name='archive_technical_task_list'),
    path('tasks/<int:pk>/archive_task_edit/', views.ArchTechnicalTaskUpdateView.as_view(), name='archive_task_edit'),
    path('disconnected-objects/', DisconnectedObjectsView.as_view(), name='disconnected_objects'),
    path('disconnected-objects/export/', export_disconnected_objects, name='export_disconnected_objects'),
    path('export_disconnected_objects_partners/export/', export_disconnected_objects_partners, name='export_disconnected_objects_partners'),
    path('archive_tasks/', ArchiveTaskListView.as_view(), name='archive_task_list'),
    path('add-skaldgsm/', views.add_skaldgsm, name='add_skaldgsm'),
    # Склад передатчик
    path('skladgsm_list/', views.skladgsm_list, name='skladgsm_list'),
    path('skladgsm/return/<int:pk>/', skladgsm_return, name='skladgsm_return'),
    path('export_kts_to_exel/', export_kts_to_exel, name='export_kts_to_exel'),
    path('export_partners_excel/', export_partners_to_excel, name='export_partners_excel'),
    path('generate_invoice/<int:pk>/', generate_invoice, name='generate_invoice'),
    path('kanban/', kanban_view, name='kanban'),
    path('kanban/update_status/<int:lead_id>/', update_lead_status, name='update_lead_status'),
    path('kanban/add-lead/', add_lead, name='add_lead'),
    path('api/create_lead/', views.create_lead, name='create_lead'),
    path('api/wazzup_webhook/', views.wazzup_webhook, name='wazzup_webhook'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

