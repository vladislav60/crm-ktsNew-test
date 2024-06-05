from django.db import models

# 9 Создание модели таблица договора
from django.urls import reverse


class kts(models.Model):
    udv_number = models.CharField(max_length=255, null=True, verbose_name="Номер УДВ")
    date_udv = models.CharField(max_length=255, null=True, verbose_name="Дата и Кем выдано")
    # company_name = models.CharField(max_length=255, verbose_name="Компания")
    company_name = models.ForeignKey('rekvizity', verbose_name="Компания", on_delete=models.PROTECT)
    dogovor_number = models.CharField(max_length=255, null=True, verbose_name="№ дог.")
    data_zakluchenia = models.CharField(max_length=255, null=True, verbose_name="Дата заключения")
    nalichiye_dogovora = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наличие Договора")
    mat_otv = models.CharField(max_length=100, null=True, verbose_name="Мат.отв")
    act_ty = models.CharField(max_length=255, blank=True, null=True, verbose_name="Акты ТУ")
    time_reag = models.IntegerField(null=True, verbose_name="Время реагирования")
    time_reag_nebol = models.IntegerField(null=True, verbose_name="Реагирование не более")
    yslovie_dogovora = models.CharField(max_length=255, blank=True, null=True, verbose_name="Условия договора")
    klient_name = models.TextField(null=True, verbose_name="Наименование Клиента")
    name_object = models.TextField(null=True, verbose_name="Наименование объекта")
    adres = models.TextField(null=True, verbose_name="Адрес объекта")
    iin_bin = models.CharField(max_length=255, null=True, blank=True, verbose_name="ИИН/БИН")
    telephone = models.TextField(null=True, verbose_name="Телефон")
    vid_sign = models.ForeignKey('vid_sign', verbose_name="Вид сигнализации", on_delete=models.PROTECT)
    urik = models.BooleanField(default=False, null=True, verbose_name="Юридическое лицо")
    chasi_po_dog = models.IntegerField(null=True, verbose_name="Часы по договору")
    dop_uslugi = models.CharField(max_length=255, blank=True, null=True, verbose_name="Алсеко")
    abon_plata = models.IntegerField(null=True, blank=True, verbose_name="Абон.плата")
    object_number = models.IntegerField(null=True, blank=True, verbose_name="№ объекта")
    peredatchik_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="№ передатчика/GSM")
    stoimost_rpo = models.IntegerField(null=True, verbose_name="Стоимость РПО")
    date_podkluchenia = models.DateField(blank=True, null=True, verbose_name="Дата подключения")
    date_otklulchenia = models.DateField(blank=True, null=True, verbose_name="Дата отключения")
    gruppa_reagirovania = models.CharField(max_length=255, blank=True, null=True, verbose_name="Группа реагирования")
    email = models.CharField(max_length=255, blank=True, null=True, verbose_name="Электронный адрес")
    vid_rpo = models.TextField(blank=True, null=True, verbose_name="Вид РПО")
    primechanie = models.TextField(blank=True, null=True, verbose_name="Примечание")
    agentskie = models.CharField(max_length=255, blank=True, null=True, verbose_name="Агентские")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото УДВ", blank=True, null=True)
    prochee = models.TextField(blank=True, null=True, verbose_name="Прочее")
    exclude_from_report = models.BooleanField(default=False, verbose_name="Не учитывать в отчете")

    def get_absolute_url(self):
        return reverse('kartochka_klienta', kwargs={'klient_id': self.pk})

    # Меняет название в админке
    class Meta:
        verbose_name = "База договоров"
        verbose_name_plural = "База договоров"
        ordering = ['-pk']


class rekvizity(models.Model):
    polnoe_name = models.CharField(max_length=255, null=True, verbose_name="Полное название компании")
    adres_company = models.CharField(max_length=255, null=True, verbose_name="Адрес компании")
    bin = models.CharField(max_length=255, null=True, verbose_name="БИН")
    iban = models.CharField(max_length=255, null=True, verbose_name="IBAN")
    bic = models.CharField(max_length=255, null=True, verbose_name="BIC")
    bank = models.CharField(max_length=255, null=True, verbose_name="BANK")
    telephone_ofiice = models.CharField(max_length=255, null=True, verbose_name="Телефон офиса")
    telephone_buh = models.CharField(max_length=255, null=True, verbose_name="Телефон бухгалтерии")
    vid_too = models.CharField(max_length=255, null=True, verbose_name="Вид ТОО")
    doljnost = models.CharField(max_length=255, null=True, verbose_name="Должность")
    ucheriditel_name_polnoe = models.CharField(max_length=255, null=True, verbose_name="ФИО директора")
    ucheriditel_name_sokr = models.CharField(max_length=255, null=True, verbose_name="ФИО директора сокращенно")

    def __str__(self):
        return self.polnoe_name

    class Meta:
        verbose_name = "Реквизиты компаний"
        verbose_name_plural = "Реквизиты компании"


class vid_sign(models.Model):
    name_sign = models.CharField(max_length=255, null=True, verbose_name="Вид сигнализации")
    name_sign_polnoe = models.CharField(max_length=255, null=True, verbose_name="Полное имя сигнализации")

    def __str__(self):
        return self.name_sign

    class Meta:
        verbose_name = "Вид сигнализации"
        verbose_name_plural = "Вид сигнализации"


class ekipazh(models.Model):
    ekipazh_name = models.CharField(max_length=255, null=True, verbose_name="Название экипажа")

    def __str__(self):
        return self.ekipazh_name

    class Meta:
        verbose_name = "Экипажи"
        verbose_name_plural = "Экипажи"


class AdditionalService(models.Model):
    # Foreign key to link the additional service to the client
    kts = models.ForeignKey(kts, on_delete=models.CASCADE, related_name='additional_services')

    # Fields for additional service information
    service_name = models.CharField(max_length=255, verbose_name="Название доп.услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    date_added = models.DateField(blank=True, null=True, verbose_name="Дата подключения")
    date_unsubscribe = models.DateField(blank=True, null=True, verbose_name="Дата отключения")

    class Meta:
        verbose_name = "Доп.Услуги"
        verbose_name_plural = "Доп.Услуги"
        ordering = ['-pk']


class partners_object(models.Model):
    object_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер объекта")
    gsm_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Номер GSM")
    name_object = models.CharField(max_length=200, blank=True, null=True, verbose_name="Наименование клиента")
    adres = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    type_object = models.CharField(max_length=100, blank=True, null=True, verbose_name="Тип объекта")
    vid_sign = models.ForeignKey('vid_sign', verbose_name="Вид сигнализации", on_delete=models.PROTECT)
    hours_mounth = models.IntegerField(null=True, blank=True, verbose_name="Часы в месяц")
    date_podkluchenia = models.DateField(null=True, blank=True, verbose_name="Дата подключения")
    tariff_per_mounth = models.FloatField(null=True, blank=True, verbose_name="Тариф за мониторинг и реагирвание в месяц")
    tehnical_services = models.BooleanField(default=False, null=True, verbose_name="Тех.обслуживание")
    rent_gsm = models.BooleanField(default=False, null=True, verbose_name="Аренда GSM")
    fire_alarm = models.BooleanField(default=False, null=True, verbose_name="Пожарная сигналзиция")
    telemetria = models.BooleanField(default=False, null=True, verbose_name="Телеметрия")
    nabludenie = models.BooleanField(default=False, null=True, verbose_name="Наблюдение")
    sms_uvedomlenie = models.BooleanField(default=False, null=True, verbose_name="SMS уведомление")
    sms_number = models.IntegerField(null=True, blank=True, verbose_name="SMS кол-во номеров")
    kolvo_day = models.IntegerField(null=True, blank=True, verbose_name="Кол-во дней")
    primechanie = models.TextField(blank=True, null=True, verbose_name="Примечание")
    ekipazh = models.ForeignKey('ekipazh', verbose_name="Экипаж", on_delete=models.SET_NULL, null=True, blank=True)
    urik = models.BooleanField(default=False, null=True, verbose_name="Юридическое лицо")
    company_name = models.ForeignKey('partners_rekvizity', verbose_name="Партнеры", on_delete=models.PROTECT)
    date_otkluchenia = models.DateField(null=True, blank=True, verbose_name="Дата отключения")

    def get_absolute_url(self):
        return reverse('kartochka_partner', kwargs={'partner_klient_id': self.pk})

    class Meta:
        verbose_name = "Объекты партнеров"
        verbose_name_plural = "Объекты партнеров"
        ordering = ['-pk']


class partners_rekvizity(models.Model):
    tehnic_srv_cost_ur = models.IntegerField(null=True, blank=True, verbose_name="Стоимость тех обслуживания Юр.лица")
    tehnic_srv_cost_fiz = models.IntegerField(null=True, blank=True, verbose_name="Стоимость тех обслуживания Физ.лица")
    pozharka_fiz = models.IntegerField(null=True, blank=True, verbose_name="Пожарная сигналзиция Физ.лица")
    pozharka_ur = models.IntegerField(null=True, blank=True, verbose_name="Пожарная сигналзиция Юр.лица")
    nabludenie_fiz = models.IntegerField(null=True, blank=True, verbose_name="Наблюдение Физ.лица")
    nabludenie_kv = models.IntegerField(null=True, blank=True, verbose_name="Наблюдение Физ.лица квартира")
    nabludenie_dom = models.IntegerField(null=True, blank=True, verbose_name="Наблюдение Физ.лица дом")
    nabludenie_ur = models.IntegerField(null=True, blank=True, verbose_name="Наблюдение Юр.лица")
    arenda_fiz = models.IntegerField(null=True, blank=True, verbose_name="Аренда GSM Физ.лица")
    arenda_ur = models.IntegerField(null=True, blank=True, verbose_name="Аренда GSM Юр.лица")
    telemetria = models.IntegerField(null=True, blank=True, verbose_name="Телеметрия")
    sms = models.IntegerField(null=True, blank=True, verbose_name="SMS")
    sms_ur = models.IntegerField(null=True, blank=True, verbose_name="SMS Юрики")
    polnoe_name = models.CharField(max_length=255, null=True, verbose_name="Полное название компании")
    adres_company = models.CharField(max_length=255, null=True, verbose_name="Адрес компании")
    bin = models.CharField(max_length=255, null=True, verbose_name="БИН")
    iban = models.CharField(max_length=255, null=True, verbose_name="IBAN")
    bic = models.CharField(max_length=255, null=True, verbose_name="BIC")
    bank = models.CharField(max_length=255, null=True, verbose_name="BANK")
    telephone_ofiice = models.CharField(max_length=255, null=True, verbose_name="Телефон офиса")
    telephone_buh = models.CharField(max_length=255, null=True, verbose_name="Телефон бухгалтерии")
    vid_too = models.CharField(max_length=255, null=True, verbose_name="Вид ТОО")
    doljnost = models.CharField(max_length=255, null=True, verbose_name="Должность")
    ucheriditel_name_polnoe = models.CharField(max_length=255, null=True, verbose_name="ФИО директора")
    ucheriditel_name_sokr = models.CharField(max_length=255, null=True, verbose_name="ФИО директора сокращенно")

    def __str__(self):
        return self.polnoe_name

    class Meta:
        verbose_name = "Реквизиты партнеров"
        verbose_name_plural = "Реквизиты партнеров"