# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse


class AlarmSchedules(models.Model):
    dtype = models.CharField(max_length=31)
    clazz = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    enabled = models.BooleanField()
    fridayenabled = models.BooleanField()
    fridayend = models.TimeField(blank=True, null=True)
    fridaystart = models.TimeField(blank=True, null=True)
    mondayenabled = models.BooleanField()
    mondayend = models.TimeField(blank=True, null=True)
    mondaystart = models.TimeField(blank=True, null=True)
    saturdayenabled = models.BooleanField()
    saturdayend = models.TimeField(blank=True, null=True)
    saturdaystart = models.TimeField(blank=True, null=True)
    sundayenabled = models.BooleanField()
    sundayend = models.TimeField(blank=True, null=True)
    sundaystart = models.TimeField(blank=True, null=True)
    thursdayenabled = models.BooleanField()
    thursdayend = models.TimeField(blank=True, null=True)
    thursdaystart = models.TimeField(blank=True, null=True)
    tuesdayenabled = models.BooleanField()
    tuesdayend = models.TimeField(blank=True, null=True)
    tuesdaystart = models.TimeField(blank=True, null=True)
    wednesdayenabled = models.BooleanField()
    wednesdayend = models.TimeField(blank=True, null=True)
    wednesdaystart = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarm_schedules'


class Alarms(models.Model):
    accepteddate = models.DateTimeField(blank=True, null=True)
    arrivaldate = models.DateTimeField(blank=True, null=True)
    cause = models.CharField(max_length=256, blank=True, null=True)
    closed = models.BooleanField()
    closeddate = models.DateTimeField(blank=True, null=True)
    createddate = models.DateTimeField(blank=True, null=True)
    report = models.CharField(max_length=1024, blank=True, null=True)
    crewid = models.ForeignKey('Users', models.DO_NOTHING, db_column='crewid')
    objectid = models.ForeignKey('GuardedObjects', models.DO_NOTHING, db_column='objectid', blank=True, null=True)
    operatorid = models.ForeignKey('Users', models.DO_NOTHING, db_column='operatorid', related_name='alarms_operatorid_set')
    zones = models.CharField(max_length=255, blank=True, null=True)
    confirmeddate = models.DateTimeField(blank=True, null=True)
    technicianreport = models.CharField(max_length=1024, blank=True, null=True)
    clazz = models.CharField(max_length=32, blank=True, null=True)
    customcause = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alarms'


class Authorities(models.Model):
    username = models.CharField(max_length=255)
    authority = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authorities'


class Causes(models.Model):
    clazz = models.CharField(max_length=31)
    title = models.CharField(max_length=128, blank=True, null=True)
    section = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'causes'


class Files(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    ext = models.CharField(max_length=255, blank=True, null=True)
    hash = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    uploadtime = models.DateTimeField(blank=True, null=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userid', blank=True, null=True)
    objectid = models.ForeignKey('GuardedObjects', models.DO_NOTHING, db_column='objectid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'files'


class GuardedObjects(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    addressbycoords = models.CharField(max_length=255, blank=True, null=True, verbose_name="Путо в базе")
    addressintersection = models.CharField(max_length=255, blank=True, null=True, verbose_name="Пересечение улиц")
    arrivingtime = models.CharField(max_length=255, blank=True, null=True, verbose_name="Время прибытия")
    connectionfrom = models.DateTimeField(blank=True, null=True, verbose_name="Дата подключения")
    contract = models.CharField(max_length=255, blank=True, null=True, verbose_name="Не используется")
    contractnumber = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер договора")
    created = models.DateTimeField(blank=True, null=True, verbose_name="Дата добавления на сайт")
    crew = models.CharField(max_length=255, blank=True, null=True, verbose_name="Экипаж")
    description = models.CharField(max_length=2048, blank=True, null=True, verbose_name="Описание объекта")
    drivingdirections = models.CharField(max_length=2048, blank=True, null=True, verbose_name="Маршрут следования")
    floor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Этаж")
    floortotal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Этажей всего:")
    forcecode = models.CharField(max_length=255, blank=True, null=True, verbose_name="Не используется")
    guardtime = models.CharField(max_length=255, blank=True, null=True, verbose_name="Не исползьзуется")
    haskeys = models.CharField(max_length=255, blank=True, null=True, verbose_name="Не исползьзуется")
    importance = models.CharField(max_length=255, blank=True, null=True, verbose_name="Степень важности объекта")
    intercomcode = models.CharField(max_length=255, blank=True, null=True, verbose_name="Код домофона")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Этаж")
    legalentity = models.BooleanField(verbose_name="Юрик")
    literal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Литер")
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя клиента")
    number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер объекта")
    objectenterways = models.CharField(max_length=255, blank=True, null=True, verbose_name="Не используется")
    reactionfrom = models.DateTimeField(blank=True, null=True, verbose_name="Не исользуется")
    schemaauthor = models.CharField(max_length=255, blank=True, null=True, verbose_name="Схему составил")
    type = models.CharField(max_length=255, blank=True, null=True, verbose_name="Тип объекта")
    cardfileid = models.ForeignKey(Files, models.DO_NOTHING, db_column='cardfileid', blank=True, null=True, verbose_name="Скачать файл карточки")
    companyid = models.ForeignKey('Users', models.DO_NOTHING, db_column='companyid', blank=True, null=True, verbose_name="Компания")
    createdbyid = models.ForeignKey('Users', models.DO_NOTHING, db_column='createdbyid', related_name='guardedobjects_createdbyid_set', blank=True, null=True)
    alarmscheduleid = models.ForeignKey(AlarmSchedules, models.DO_NOTHING, db_column='alarmscheduleid', blank=True, null=True)
    firescheduleid = models.ForeignKey(AlarmSchedules, models.DO_NOTHING, db_column='firescheduleid', related_name='guardedobjects_firescheduleid_set', blank=True, null=True)
    securityscheduleid = models.ForeignKey(AlarmSchedules, models.DO_NOTHING, db_column='securityscheduleid', related_name='guardedobjects_securityscheduleid_set', blank=True, null=True)
    technician = models.CharField(max_length=255, blank=True, null=True, verbose_name="Участок техника")
    pdfgenerated = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    titlephotoid = models.ForeignKey(Files, models.DO_NOTHING, db_column='titlephotoid', related_name='guardedobjects_titlephotoid_set', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('guardedobject_detail', kwargs={'pk': self.pk})

    class Meta:
        managed = False
        db_table = 'guarded_objects'


class GuardedZones(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=255, blank=True, null=True)
    resources = models.CharField(max_length=255, blank=True, null=True)
    objectid = models.ForeignKey(GuardedObjects, models.DO_NOTHING, db_column='objectid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guarded_zones'


class LetterCounters(models.Model):
    count = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'letter_counters'


class Roles(models.Model):
    isgroup = models.BooleanField()
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class UserRole(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_role'


class Users(models.Model):
    enabled = models.BooleanField()
    lastlogindate = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    sessionttl = models.IntegerField()
    username = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersSessions(models.Model):
    primary_id = models.CharField(max_length=36)
    session_id = models.CharField(max_length=36)
    creation_time = models.BigIntegerField()
    last_access_time = models.BigIntegerField()
    max_inactive_interval = models.IntegerField()
    expiry_time = models.BigIntegerField()
    principal_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_sessions'


class UsersSessionsAttributes(models.Model):
    session_primary_id = models.CharField(max_length=36)
    attribute_name = models.CharField(max_length=200)
    attribute_bytes = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'users_sessions_attributes'


class Words(models.Model):
    clazz = models.CharField(max_length=31)
    name = models.CharField(max_length=255)
    companyid = models.ForeignKey(Users, models.DO_NOTHING, db_column='companyid', blank=True, null=True)
    json = models.CharField(max_length=255, blank=True, null=True)
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='userid', related_name='words_userid_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'words'
