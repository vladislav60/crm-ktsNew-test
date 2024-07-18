# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ademcoe(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime', db_comment='Время приема сообщения на клие')  # Field name made lowercase.
    receivern = models.CharField(db_column='ReceiverN', max_length=50, db_comment='Номер сообщения??(не используе')  # Field name made lowercase.
    linecardgroupn = models.CharField(db_column='LineCardGroupN', max_length=50, db_comment='Номер линейной платы????(не ис')  # Field name made lowercase.
    unitn = models.CharField(db_column='UnitN', max_length=50, db_comment='Номер устройства')  # Field name made lowercase.
    messagetypeid = models.CharField(db_column='MessageTypeID', max_length=50, db_comment='Тип сообщения ????? Возможно н')  # Field name made lowercase.
    eventid = models.CharField(db_column='EventID', max_length=50, db_comment='Тип и номер события')  # Field name made lowercase.
    groupn = models.CharField(db_column='GroupN', max_length=50, db_comment='Номер раздела (зависит от типа')  # Field name made lowercase.
    sensorid = models.CharField(db_column='SensorID', max_length=50, db_comment='Номер зоны(или отвестенного ил')  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADEMCOE'


class Adtypes(models.Model):
    panel = models.IntegerField(db_column='PANEL', primary_key=True, db_comment='Тип панели или адаптера')  # Field name made lowercase.
    desc = models.CharField(db_column='DESC', max_length=250, db_comment='Название')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADTYPES'


class Aesevents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    aescode = models.CharField(db_column='AESCODE', max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100)  # Field name made lowercase.
    sensor = models.IntegerField(db_column='SENSOR', blank=True, null=True)  # Field name made lowercase.
    eventcod = models.IntegerField(db_column='EVENTCOD')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AESEVENTS'


class Alarme(models.Model):
    alarmid = models.AutoField(db_column='AlarmID', primary_key=True, db_comment='ID тревоги')  # Field name made lowercase.
    zoneid = models.ForeignKey('Zones', db_column='ZoneID', db_comment='ID зоны', on_delete=models.CASCADE,
                               related_name='alarms')
    userid = models.IntegerField(db_column='UserID', blank=True, null=True, db_comment='ID оператора (userа)')  # Field name made lowercase.
    state = models.IntegerField(db_column='State', db_comment='Состояние - неподтвержденная, ')  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime', blank=True, null=True, db_comment='Время приема тревожного событи')  # Field name made lowercase.
    confirmtime = models.DateTimeField(db_column='ConfirmTime', blank=True, null=True, db_comment='Время подтверждения')  # Field name made lowercase.
    processtime = models.DateTimeField(db_column='ProcessTime', blank=True, null=True, db_comment='Время отработки')  # Field name made lowercase.
    recovertime = models.DateTimeField(db_column='RecoverTime', blank=True, null=True, db_comment='Время восстановления зоны')  # Field name made lowercase.
    lastreceivetime = models.DateTimeField(db_column='LastReceiveTime', blank=True, null=True, db_comment='Время приема последней тревоги')  # Field name made lowercase.
    receivecount = models.IntegerField(db_column='ReceiveCount', db_comment='Сколько раз срабатывала тревог')  # Field name made lowercase.
    reason = models.ForeignKey('Reasons', db_column='Reason', blank=True, null=True, db_comment='Причина срабатывания (отработк)', related_name='reason', on_delete=models.CASCADE)  # Field name made lowercase.
    sendtime_deg = models.DateTimeField(db_column='SendTime_Deg', blank=True, null=True, db_comment='Время отправки тревоги в ЕКЦ')  # Field name made lowercase.
    receivetime_deg = models.DateTimeField(db_column='ReceiveTime_Deg', blank=True, null=True, db_comment='Время приема дежурной частью( ')  # Field name made lowercase.
    confirmtime_deg = models.DateTimeField(db_column='ConfirmTime_Deg', blank=True, null=True, db_comment='Время отработки дежурной часть')  # Field name made lowercase.
    receivetime_omc = models.DateTimeField(db_column='ReceiveTime_OMC', blank=True, null=True)  # Field name made lowercase.
    confirmtime_omc = models.DateTimeField(db_column='ConfirmTime_OMC', blank=True, null=True)  # Field name made lowercase.
    rowid = models.TextField(db_column='RowID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', blank=True, null=True)  # Field name made lowercase.
    processtime_deg = models.DateTimeField(db_column='ProcessTime_Deg', blank=True, null=True)  # Field name made lowercase.
    done_e = models.IntegerField(db_column='DONE_E', blank=True, null=True)  # Field name made lowercase.
    crew_arr = models.DateTimeField(db_column='Crew_Arr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ALARME'


class Alarmprim(models.Model):
    alarmid = models.IntegerField(db_column='AlarmID', primary_key=True)  # Field name made lowercase.
    crew_arr = models.DateTimeField(db_column='Crew_Arr', blank=True, null=True)  # Field name made lowercase.
    prim = models.CharField(db_column='Prim', max_length=250, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ALARMPrim'


class AllIm(models.Model):
    modul = models.FloatField(db_column='MODUL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ALL_IM'


class Archalarme(models.Model):
    alarmid = models.IntegerField(db_column='AlarmID')  # Field name made lowercase.
    zoneid = models.IntegerField(db_column='ZoneID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State')  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime', blank=True, null=True)  # Field name made lowercase.
    confirmtime = models.DateTimeField(db_column='ConfirmTime', blank=True, null=True)  # Field name made lowercase.
    processtime = models.DateTimeField(db_column='ProcessTime', blank=True, null=True)  # Field name made lowercase.
    recovertime = models.DateTimeField(db_column='RecoverTime', blank=True, null=True)  # Field name made lowercase.
    lastreceivetime = models.DateTimeField(db_column='LastReceiveTime', blank=True, null=True)  # Field name made lowercase.
    receivecount = models.IntegerField(db_column='ReceiveCount')  # Field name made lowercase.
    reason = models.IntegerField(db_column='Reason', blank=True, null=True)  # Field name made lowercase.
    sendtime_deg = models.DateTimeField(db_column='SendTime_Deg', blank=True, null=True)  # Field name made lowercase.
    receivetime_deg = models.DateTimeField(db_column='ReceiveTime_Deg', blank=True, null=True)  # Field name made lowercase.
    confirmtime_deg = models.DateTimeField(db_column='ConfirmTime_Deg', blank=True, null=True)  # Field name made lowercase.
    receivetime_omc = models.DateTimeField(db_column='ReceiveTime_OMC', blank=True, null=True)  # Field name made lowercase.
    confirmtime_omc = models.DateTimeField(db_column='ConfirmTime_OMC', blank=True, null=True)  # Field name made lowercase.
    rowid = models.TextField(db_column='RowID', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', blank=True, null=True)  # Field name made lowercase.
    processtime_deg = models.DateTimeField(db_column='ProcessTime_Deg', blank=True, null=True)  # Field name made lowercase.
    done_e = models.IntegerField(db_column='DONE_E', blank=True, null=True)  # Field name made lowercase.
    crew_arr = models.DateTimeField(db_column='Crew_Arr', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHALARME'


class Archalarmprim(models.Model):
    alarmid = models.IntegerField(db_column='AlarmID', primary_key=True)  # Field name made lowercase.
    crew_arr = models.DateTimeField(db_column='Crew_Arr', blank=True, null=True)  # Field name made lowercase.
    prim = models.CharField(db_column='Prim', max_length=250, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHALARMPrim'


class Archgsmmsg(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BASENUMBER')  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GROUPN', blank=True, null=True)  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE', blank=True, null=True)  # Field name made lowercase.
    event = models.CharField(db_column='EVENT', max_length=4)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD')  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHGSMMSG'


class Archktmmsg(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    rep = models.IntegerField(db_column='REP')  # Field name made lowercase.
    num = models.IntegerField(db_column='NUM')  # Field name made lowercase.
    numr = models.IntegerField(db_column='NUMR', blank=True, null=True)  # Field name made lowercase.
    msg = models.CharField(db_column='MSG', max_length=8)  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD', blank=True, null=True)  # Field name made lowercase.
    ademco = models.CharField(db_column='ADEMCO', max_length=26)  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHKTMMSG'


class Archothere(models.Model):
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    cardid = models.IntegerField(db_column='CARDID')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=60)  # Field name made lowercase.
    eventtype = models.IntegerField(db_column='EventType')  # Field name made lowercase.
    sensorid = models.IntegerField(db_column='SensorID')  # Field name made lowercase.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    done = models.IntegerField(db_column='Done', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHOTHERE'


class Archstat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    av = models.DecimalField(db_column='AV', max_digits=18, decimal_places=2)  # Field name made lowercase.
    mx = models.DecimalField(db_column='MX', max_digits=18, decimal_places=2)  # Field name made lowercase.
    mn = models.DecimalField(db_column='MN', max_digits=18, decimal_places=2)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    numrl = models.IntegerField(db_column='NUMRL')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHSTAT'


class Archwatche(models.Model):
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    responsibleid = models.IntegerField(db_column='ResponsibleID')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID')  # Field name made lowercase.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHWATCHE'


class ArchGsm2History(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL', blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT')  # Field name made lowercase.
    sq = models.IntegerField(db_column='SQ')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dis = models.DateTimeField(db_column='DIS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCH_GSM2_HISTORY'


class ArchtblEvents(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime')  # Field name made lowercase.
    basen = models.IntegerField(db_column='BaseN')  # Field name made lowercase.
    unitn = models.IntegerField(db_column='UnitN')  # Field name made lowercase.
    eventkind = models.CharField(db_column='EventKind', max_length=10)  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GroupN')  # Field name made lowercase.
    sensorn = models.IntegerField(db_column='SensorN')  # Field name made lowercase.
    workstationn = models.IntegerField(db_column='WorkstationN', blank=True, null=True)  # Field name made lowercase.
    rowver = models.TextField(db_column='RowVer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARCHtbl_Events'


class Aud(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    tablename = models.CharField(db_column='TABLENAME', max_length=200)  # Field name made lowercase.
    operation = models.CharField(db_column='OPERATION', max_length=1)  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True)  # Field name made lowercase.
    recid = models.IntegerField(db_column='RECID')  # Field name made lowercase.
    recid2 = models.IntegerField(db_column='RECID2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AUD'


class Bases(models.Model):
    baseid = models.IntegerField(db_column='BaseID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=50, db_comment='Имя Системы')  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dir = models.CharField(db_column='DIR', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BASES'


class BaseUnittype(models.Model):
    base = models.IntegerField(db_column='BASE', primary_key=True)  # Field name made lowercase. The composite primary key (BASE, UNITTYPE) found, that is not supported. The first column is selected.
    unittype = models.IntegerField(db_column='UNITTYPE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BASE_UNITTYPE'
        unique_together = (('base', 'unittype'),)


class Cards(models.Model):
    cardid = models.AutoField(db_column='CARDID', primary_key=True)  # Field name made lowercase.
    basenumber = models.ForeignKey('Bases', db_column='BASENUMBER', db_comment='Номер базы', on_delete=models.CASCADE)  # Дабавил Key
    otisnumber = models.IntegerField(db_column='OTISNUMBER', db_comment='Номер договора')  # Field name made lowercase.
    objectname = models.CharField(db_column='OBJECTNAME', max_length=250, db_comment='Наименование объекта, владелец')  # Field name made lowercase.
    callsign = models.CharField(db_column='CALLSIGN', max_length=10, blank=True, null=True, db_comment='Позывной группы реагирования')  # Field name made lowercase.
    callnumber = models.IntegerField(db_column='CALLNUMBER', blank=True, null=True, db_comment='Номер группы реагирования')  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=255, db_comment='Адрес и инофрмация об объекте')  # Field name made lowercase.
    particularity = models.CharField(db_column='PARTICULARITY', max_length=500, blank=True, null=True, db_comment='Особенности объекта')  # Field name made lowercase.
    phones = models.CharField(db_column='PHONES', max_length=255, blank=True, null=True, db_comment='Номер телефона клиента')  # Field name made lowercase.
    scheme = models.BinaryField(db_column='SCHEME', blank=True, null=True, db_comment='Схема расположения объекта')  # Field name made lowercase.
    unitnumber = models.IntegerField(db_column='UNITNUMBER', blank=True, null=True, db_comment='Номер модуля')  # Field name made lowercase.
    unittype = models.ForeignKey('Unittype', db_column='UNITTYPE', blank=True, null=True, on_delete=models.CASCADE)
    zonesstate = models.IntegerField(db_column='ZONESSTATE', blank=True, null=True)  # Field name made lowercase.
    isprotected = models.CharField(db_column='ISPROTECTED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gsmphone = models.CharField(db_column='GSMPHONE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    workstation = models.IntegerField(db_column='WORKSTATION', blank=True, null=True)  # Field name made lowercase.
    orgid = models.ForeignKey('Org', db_column='ORGID', blank=True, null=True, on_delete=models.SET_NULL)  # Field name made lowercase.
    agreement = models.CharField(db_column='AGREEMENT', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lost = models.IntegerField(db_column='LOST', blank=True, null=True)  # Field name made lowercase.
    test = models.IntegerField(db_column='TEST', blank=True, null=True)  # Field name made lowercase.
    flags = models.IntegerField(db_column='FLAGS', blank=True, null=True)  # Field name made lowercase.
    lat = models.DecimalField(db_column='LAT', max_digits=13, decimal_places=10, blank=True, null=True)  # Field name made lowercase.
    lon = models.DecimalField(db_column='LON', max_digits=13, decimal_places=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CARDS'
        app_label = 'pult'
        unique_together = (('otisnumber', 'orgid'),)


class CardsLog(models.Model):
    cardid = models.IntegerField(db_column='CARDID', blank=True, null=True)  # Field name made lowercase.
    basenumberu = models.IntegerField(db_column='BASENUMBERU', blank=True, null=True)  # Field name made lowercase.
    otisnumberu = models.IntegerField(db_column='OTISNUMBERU', blank=True, null=True)  # Field name made lowercase.
    unitnumberu = models.IntegerField(db_column='UNITNUMBERU', blank=True, null=True)  # Field name made lowercase.
    unittypeu = models.IntegerField(db_column='UNITTYPEU', blank=True, null=True)  # Field name made lowercase.
    isprotectedu = models.CharField(db_column='ISPROTECTEDU', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workstationu = models.IntegerField(db_column='WORKSTATIONU', blank=True, null=True)  # Field name made lowercase.
    orgidu = models.IntegerField(db_column='ORGIDU', blank=True, null=True)  # Field name made lowercase.
    lostu = models.IntegerField(db_column='LOSTU', blank=True, null=True)  # Field name made lowercase.
    testu = models.IntegerField(db_column='TESTU', blank=True, null=True)  # Field name made lowercase.
    basenumberd = models.IntegerField(db_column='BASENUMBERD', blank=True, null=True)  # Field name made lowercase.
    otisnumberd = models.IntegerField(db_column='OTISNUMBERD', blank=True, null=True)  # Field name made lowercase.
    unitnumberd = models.IntegerField(db_column='UNITNUMBERD', blank=True, null=True)  # Field name made lowercase.
    unittyped = models.IntegerField(db_column='UNITTYPED', blank=True, null=True)  # Field name made lowercase.
    isprotectedd = models.CharField(db_column='ISPROTECTEDD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    workstationd = models.IntegerField(db_column='WORKSTATIOND', blank=True, null=True)  # Field name made lowercase.
    orgidd = models.IntegerField(db_column='ORGIDD', blank=True, null=True)  # Field name made lowercase.
    lostd = models.IntegerField(db_column='LOSTD', blank=True, null=True)  # Field name made lowercase.
    testd = models.IntegerField(db_column='TESTD', blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    objectnameu = models.CharField(db_column='OBJECTNAMEU', max_length=250, blank=True, null=True)  # Field name made lowercase.
    objectnamed = models.CharField(db_column='OBJECTNAMED', max_length=250, blank=True, null=True)  # Field name made lowercase.
    infou = models.CharField(db_column='INFOU', max_length=255, blank=True, null=True)  # Field name made lowercase.
    infod = models.CharField(db_column='INFOD', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CARDS_LOG'


class Errore(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime')  # Field name made lowercase.
    basen = models.IntegerField(db_column='BaseN')  # Field name made lowercase.
    unitn = models.IntegerField(db_column='UnitN')  # Field name made lowercase.
    eventkind = models.CharField(db_column='EventKind', max_length=10)  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GroupN')  # Field name made lowercase.
    sensorn = models.IntegerField(db_column='SensorN')  # Field name made lowercase.
    workstationn = models.IntegerField(db_column='WorkstationN')  # Field name made lowercase.
    error = models.IntegerField(db_column='Error')  # Field name made lowercase.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    loginid = models.IntegerField(db_column='LOGINID', blank=True, null=True)  # Field name made lowercase.
    login = models.CharField(db_column='LOGIN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    hostip = models.CharField(db_column='HOSTIP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERRORE'


class ErroreLog(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid = models.IntegerField(db_column='EventID')  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime')  # Field name made lowercase.
    basen = models.IntegerField(db_column='BaseN')  # Field name made lowercase.
    unitn = models.IntegerField(db_column='UnitN')  # Field name made lowercase.
    eventkind = models.CharField(db_column='EventKind', max_length=10)  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GroupN')  # Field name made lowercase.
    sensorn = models.IntegerField(db_column='SensorN')  # Field name made lowercase.
    workstationn = models.IntegerField(db_column='WorkstationN')  # Field name made lowercase.
    error = models.IntegerField(db_column='Error')  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    hostip = models.CharField(db_column='HOSTIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    delete_time = models.DateTimeField(db_column='DELETE_TIME')  # Field name made lowercase.
    loginid = models.IntegerField(db_column='LOGINID')  # Field name made lowercase.
    login = models.CharField(db_column='LOGIN', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERRORE_LOG'


class Errortype(models.Model):
    err = models.IntegerField(db_column='ERR', primary_key=True)  # Field name made lowercase.
    e_disc = models.CharField(db_column='E_DISC', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERRORTYPE'


class Eventtypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EVENTTYPES'


class ENames(models.Model):
    key_id = models.AutoField(db_column='KEY_ID', primary_key=True)  # Field name made lowercase.
    e_number = models.CharField(db_column='E_NUMBER', unique=True, max_length=8, blank=True, null=True)  # Field name made lowercase.
    e_name = models.CharField(db_column='E_NAME', max_length=11, blank=True, null=True)  # Field name made lowercase.
    e_name_eng = models.CharField(db_column='E_NAME_ENG', max_length=11, blank=True, null=True)  # Field name made lowercase.
    e_name_lat = models.CharField(db_column='E_NAME_LAT', max_length=11, blank=True, null=True)  # Field name made lowercase.
    e_disc = models.CharField(db_column='E_DISC', max_length=80, blank=True, null=True)  # Field name made lowercase.
    e_denglish = models.CharField(db_column='E_DENGLISH', max_length=80, blank=True, null=True)  # Field name made lowercase.
    e_dlatvian = models.CharField(db_column='E_DLATVIAN', max_length=80, blank=True, null=True)  # Field name made lowercase.
    alarm = models.CharField(db_column='ALARM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    techno = models.CharField(db_column='TECHNO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    service = models.CharField(db_column='SERVICE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    th1 = models.CharField(db_column='TH1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pl = models.CharField(db_column='PL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    arming = models.CharField(db_column='ARMING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    disarming = models.CharField(db_column='DISARMING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pult = models.CharField(db_column='PULT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    f_color = models.IntegerField(db_column='F_Color', blank=True, null=True)  # Field name made lowercase.
    paneltype = models.CharField(db_column='PanelType', max_length=5, blank=True, null=True)  # Field name made lowercase.
    zone_n = models.SmallIntegerField(db_column='Zone_n', blank=True, null=True)  # Field name made lowercase.
    rajon = models.SmallIntegerField(db_column='Rajon', blank=True, null=True)  # Field name made lowercase.
    type_ev = models.SmallIntegerField(db_column='Type_Ev', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'E_NAMES'


class Gforce(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GFORCE'


class Gsm2Msg(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    b1 = models.IntegerField(db_column='B1', blank=True, null=True)  # Field name made lowercase.
    b2 = models.IntegerField(db_column='B2', blank=True, null=True)  # Field name made lowercase.
    b3 = models.IntegerField(db_column='B3', blank=True, null=True)  # Field name made lowercase.
    b4 = models.IntegerField(db_column='B4', blank=True, null=True)  # Field name made lowercase.
    sq = models.IntegerField(db_column='SQ', blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD', blank=True, null=True)  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.
    sms = models.IntegerField(db_column='SMS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2MSG'


class Gsm2Cmd(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=50)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', db_comment='флаг подтверждения 0 - новый п')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    n = models.IntegerField(db_column='N', blank=True, null=True)  # Field name made lowercase.
    srv = models.IntegerField(db_column='SRV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_CMD'


class Gsm2CmdLog(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', db_comment='флаг подтверждения 0 - новый п')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    idt = models.DateTimeField(db_column='IDT', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_CMD_LOG'


class Gsm2CmdLogOp(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sn_cmd = models.CharField(db_column='SN_CMD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', db_comment='флаг подтверждения 0 - новый п')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    idt = models.DateTimeField(db_column='IDT', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    sn_in = models.CharField(db_column='SN_IN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    sms_in = models.BinaryField(db_column='SMS_IN', blank=True, null=True)  # Field name made lowercase.
    dt_in = models.DateTimeField(db_column='DT_IN', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_CMD_LOG_OP'


class Gsm2Egroup(models.Model):
    egroup = models.IntegerField(db_column='EGROUP', primary_key=True)  # Field name made lowercase.
    g_disc = models.CharField(db_column='G_DISC', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_EGROUP'


class Gsm2Events(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    egroup = models.IntegerField(db_column='EGROUP')  # Field name made lowercase.
    e1min = models.IntegerField(db_column='E1MIN', blank=True, null=True)  # Field name made lowercase.
    e1max = models.IntegerField(db_column='E1MAX', blank=True, null=True)  # Field name made lowercase.
    off1 = models.IntegerField(db_column='OFF1')  # Field name made lowercase.
    e2min = models.IntegerField(db_column='E2MIN', blank=True, null=True)  # Field name made lowercase.
    e2max = models.IntegerField(db_column='E2MAX', blank=True, null=True)  # Field name made lowercase.
    off2 = models.IntegerField(db_column='OFF2')  # Field name made lowercase.
    e_disc = models.CharField(db_column='E_DISC', max_length=250)  # Field name made lowercase.
    enabled = models.IntegerField(db_column='ENABLED')  # Field name made lowercase.
    acod = models.CharField(db_column='ACOD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    zu = models.IntegerField(db_column='ZU', blank=True, null=True, db_comment='0 - техно,1-польз.,2-зона')  # Field name made lowercase.
    azon = models.IntegerField(db_column='AZON', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_EVENTS'


class Gsm2History(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT')  # Field name made lowercase.
    sq = models.IntegerField(db_column='SQ')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dis = models.DateTimeField(db_column='DIS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_HISTORY'


class Gsm2In(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    cmd = models.BinaryField(db_column='CMD', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM2_IN'


class Gsmevents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    e_num = models.IntegerField(db_column='E_NUM', unique=True, db_comment='Номер(код) события')  # Field name made lowercase.
    e_name = models.CharField(db_column='E_NAME', max_length=4, db_comment='Символьный код события (AES ко')  # Field name made lowercase.
    e_conv = models.CharField(db_column='E_CONV', max_length=4, blank=True, null=True)  # Field name made lowercase.
    e_disc = models.CharField(db_column='E_DISC', max_length=255, db_comment='Описание')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSMEVENTS'


class Gsmmsg(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BASENUMBER')  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GROUPN', blank=True, null=True)  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE', blank=True, null=True)  # Field name made lowercase.
    event = models.CharField(db_column='EVENT', max_length=4)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD')  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSMMSG'


class Gsmoutobj(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=50)  # Field name made lowercase.
    event = models.IntegerField(db_column='EVENT')  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GROUPN')  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE')  # Field name made lowercase.
    basen = models.IntegerField(db_column='BASEN')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSMOUTOBJ'


class Gsmsim(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=10)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', unique=True, max_length=20)  # Field name made lowercase.
    pin1 = models.CharField(db_column='PIN1', max_length=4, blank=True, null=True)  # Field name made lowercase.
    puk1 = models.CharField(db_column='PUK1', max_length=8, blank=True, null=True)  # Field name made lowercase.
    pin2 = models.CharField(db_column='PIN2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    puk2 = models.CharField(db_column='PUK2', max_length=8, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    orgid = models.IntegerField(db_column='ORGID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSMSIM'
        unique_together = (('phone', 'id', 'sn', 'dt', 'orgid'), ('sn', 'id', 'phone', 'dt', 'orgid'),)


class GsmConn(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pid = models.CharField(db_column='PID', max_length=50)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True, db_comment='тип панели')  # Field name made lowercase.
    notservice = models.IntegerField(db_column='NOTSERVICE', blank=True, null=True, db_comment='флаг обслуживания')  # Field name made lowercase.
    sq = models.IntegerField(db_column='SQ', blank=True, null=True, db_comment='Качество связи')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT')  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD')  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT')  # Field name made lowercase.
    srv = models.IntegerField(db_column='SRV', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM_CONN'


class GsmUsn(models.Model):
    sn = models.CharField(db_column='SN', primary_key=True, max_length=20)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM_USN'


class GsmUsnLog(models.Model):
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GSM_USN_LOG'


class Hdays(models.Model):
    sectionid = models.IntegerField(db_column='SectionID', primary_key=True)  # Field name made lowercase. The composite primary key (SectionID, HDAY, HMONTH) found, that is not supported. The first column is selected.
    hday = models.IntegerField(db_column='HDAY')  # Field name made lowercase.
    hmonth = models.IntegerField(db_column='HMONTH')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HDAYS'
        unique_together = (('sectionid', 'hday', 'hmonth'),)


class HdaysLog(models.Model):
    sectionid = models.IntegerField(db_column='SectionID', blank=True, null=True)  # Field name made lowercase.
    hdayu = models.IntegerField(db_column='HDAYU', blank=True, null=True)  # Field name made lowercase.
    hmonthu = models.IntegerField(db_column='HMONTHU', blank=True, null=True)  # Field name made lowercase.
    hdayd = models.IntegerField(db_column='HDAYD', blank=True, null=True)  # Field name made lowercase.
    hmonthd = models.IntegerField(db_column='HMONTHD', blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HDAYS_LOG'


class Ktmademco(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    a_cod = models.CharField(db_column='A_COD', max_length=4)  # Field name made lowercase.
    a_disc_ru = models.CharField(db_column='A_DISC_RU', max_length=80)  # Field name made lowercase.
    a_disc_en = models.CharField(db_column='A_DISC_EN', max_length=80)  # Field name made lowercase.
    iszone = models.CharField(db_column='ISZONE', max_length=1)  # Field name made lowercase.
    arming = models.CharField(db_column='ARMING', max_length=1)  # Field name made lowercase.
    disarming = models.CharField(db_column='DISARMING', max_length=1)  # Field name made lowercase.
    batteryoff = models.CharField(db_column='BATTERYOFF', max_length=1)  # Field name made lowercase.
    batteryon = models.CharField(db_column='BATTERYON', max_length=1)  # Field name made lowercase.
    poweroff = models.CharField(db_column='POWEROFF', max_length=1)  # Field name made lowercase.
    poweron = models.CharField(db_column='POWERON', max_length=1)  # Field name made lowercase.
    firezon = models.CharField(db_column='FIREZON', max_length=1)  # Field name made lowercase.
    zonerestore = models.CharField(db_column='ZONERESTORE', max_length=1)  # Field name made lowercase.
    zonebreak = models.CharField(db_column='ZONEBREAK', max_length=1)  # Field name made lowercase.
    zoneincl = models.CharField(db_column='ZONEINCL', max_length=1)  # Field name made lowercase.
    zoneexcl = models.CharField(db_column='ZONEEXCL', max_length=1)  # Field name made lowercase.
    duress = models.CharField(db_column='DURESS', max_length=1)  # Field name made lowercase.
    abutton = models.CharField(db_column='ABUTTON', max_length=1)  # Field name made lowercase.
    acod = models.CharField(db_column='ACOD', max_length=20, blank=True, null=True)  # Field name made lowercase.
    enabled = models.CharField(db_column='ENABLED', max_length=1)  # Field name made lowercase.
    alarm = models.CharField(db_column='ALARM', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMADEMCO'


class Ktmevents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    e_number = models.CharField(db_column='E_NUMBER', unique=True, max_length=8)  # Field name made lowercase.
    e_disc = models.CharField(db_column='E_DISC', max_length=80, blank=True, null=True)  # Field name made lowercase.
    e_denglish = models.CharField(db_column='E_DENGLISH', max_length=80, blank=True, null=True)  # Field name made lowercase.
    sectionnum = models.IntegerField(db_column='SECTIONNUM', blank=True, null=True)  # Field name made lowercase.
    zonenum = models.IntegerField(db_column='ZONENUM', blank=True, null=True)  # Field name made lowercase.
    iszone = models.CharField(db_column='ISZONE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ispanel = models.CharField(db_column='ISPANEL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alarm = models.CharField(db_column='ALARM', max_length=1)  # Field name made lowercase.
    arming = models.CharField(db_column='ARMING', max_length=1)  # Field name made lowercase.
    disarming = models.CharField(db_column='DISARMING', max_length=1)  # Field name made lowercase.
    batteryoff = models.CharField(db_column='BATTERYOFF', max_length=1)  # Field name made lowercase.
    poweroff = models.CharField(db_column='POWEROFF', max_length=1)  # Field name made lowercase.
    batteryon = models.CharField(db_column='BATTERYON', max_length=1)  # Field name made lowercase.
    poweron = models.CharField(db_column='POWERON', max_length=1)  # Field name made lowercase.
    firezon = models.CharField(db_column='FIREZON', max_length=1)  # Field name made lowercase.
    zonerestore = models.CharField(db_column='ZONERESTORE', max_length=1, db_comment='Восстановление зоны')  # Field name made lowercase.
    zonebreak = models.CharField(db_column='ZONEBREAK', max_length=1, db_comment='Нарушение зоны')  # Field name made lowercase.
    zoneexcl = models.CharField(db_column='ZONEEXCL', max_length=1, db_comment='Зона исключена')  # Field name made lowercase.
    zoneincl = models.CharField(db_column='ZONEINCL', max_length=1, db_comment='Зона включена')  # Field name made lowercase.
    duress = models.CharField(db_column='DURESS', max_length=1, db_comment='Принуждение')  # Field name made lowercase.
    abutton = models.CharField(db_column='ABUTTON', max_length=1, db_comment='Тревожная кнопка нажата')  # Field name made lowercase.
    enabled = models.CharField(db_column='ENABLED', max_length=1)  # Field name made lowercase.
    acod = models.CharField(db_column='ACOD', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMEVENTS'


class Ktmmsg(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    rep = models.IntegerField(db_column='REP')  # Field name made lowercase.
    num = models.IntegerField(db_column='NUM')  # Field name made lowercase.
    numr = models.IntegerField(db_column='NUMR', blank=True, null=True)  # Field name made lowercase.
    msg = models.CharField(db_column='MSG', max_length=8)  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True)  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD', blank=True, null=True)  # Field name made lowercase.
    ademco = models.CharField(db_column='ADEMCO', max_length=26)  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMMSG'


class Ktmmsgu(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True, db_comment='дата пакета')  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BASENUMBER', db_comment='База')  # Field name made lowercase.
    rep = models.IntegerField(db_column='REP', db_comment='Ретранслятор')  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL', db_comment='Модуль')  # Field name made lowercase.
    num = models.IntegerField(db_column='NUM', db_comment='Номер пакета')  # Field name made lowercase.
    msg = models.CharField(db_column='MSG', max_length=8, db_comment='Выделенное сообщение')  # Field name made lowercase.
    ademco = models.CharField(db_column='ADEMCO', max_length=26, db_comment='Весь пакет')  # Field name made lowercase.
    sig = models.IntegerField(db_column='SIG', db_comment='Уровень сигнала')  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD', blank=True, null=True)  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMMSGU'


class Ktmstat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    num = models.IntegerField(db_column='NUM', db_comment='Номер сообщения')  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL', db_comment='Номер модуля')  # Field name made lowercase.
    rep = models.IntegerField(db_column='REP', db_comment='Ретранслятор')  # Field name made lowercase.
    numrl = models.IntegerField(db_column='NUMRL', blank=True, null=True, db_comment='Локальный приемник')  # Field name made lowercase.
    msg = models.CharField(db_column='MSG', max_length=8, blank=True, null=True, db_comment='Сообщение')  # Field name made lowercase.
    signal = models.IntegerField(db_column='SIGNAL', db_comment='Уровень сигнала')  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True, db_comment='Дата посылки')  # Field name made lowercase.
    pac = models.CharField(db_column='PAC', max_length=26)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber', db_comment='Номер базы')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMSTAT'


class Ktmstatsig(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL', db_comment='Модуль')  # Field name made lowercase.
    numrl = models.IntegerField(db_column='NUMRL', db_comment='Номер локального приемника')  # Field name made lowercase.
    rep = models.IntegerField(db_column='REP', db_comment='Ретранслятор')  # Field name made lowercase.
    signal = models.IntegerField(db_column='SIGNAL', db_comment='Уровень')  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber', db_comment='База')  # Field name made lowercase.
    cnt = models.IntegerField(db_column='CNT', blank=True, null=True)  # Field name made lowercase.
    dat = models.DateTimeField(db_column='DAT', blank=True, null=True, db_comment='Дата и время вставки')  # Field name made lowercase.
    upd = models.DateTimeField(db_column='UPD', blank=True, null=True, db_comment='Дата и время последнего приход')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMSTATSIG'


class Ktmundefmsg(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    basen = models.IntegerField(db_column='BASEN')  # Field name made lowercase.
    unitn = models.IntegerField(db_column='UNITN')  # Field name made lowercase.
    msg = models.CharField(db_column='MSG', max_length=8)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTMUNDEFMSG'


class Ktsrent(models.Model):
    орг_я = models.CharField(db_column='Орг-я', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    imei = models.CharField(db_column='IMEI', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KTSRENT'


class Leftusn(models.Model):
    sn = models.CharField(db_column='SN', primary_key=True, max_length=20)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LEFTUSN'


class Loge(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True, db_comment='ID события регистрации (Login/')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', db_comment='ID оператора (userа)')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', db_comment='Тип регистрации (Login/Logout)')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', db_comment='Время регистрации')  # Field name made lowercase.
    workstationn = models.IntegerField(db_column='WorkStationN')  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LOGE'


class Messages(models.Model):
    messageid = models.AutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type')  # Field name made lowercase.
    kind = models.IntegerField(db_column='Kind')  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=50)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BaseNumber')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MESSAGES'


class Moduls(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    base = models.IntegerField(db_column='BASE')  # Field name made lowercase.
    unittype = models.IntegerField(db_column='UNITTYPE')  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True)  # Field name made lowercase.
    notserv = models.IntegerField(db_column='NOTSERV', blank=True, null=True)  # Field name made lowercase.
    clpacketid = models.IntegerField(db_column='CLPACKETID', blank=True, null=True)  # Field name made lowercase.
    np = models.IntegerField(db_column='NP', blank=True, null=True)  # Field name made lowercase.
    eth = models.IntegerField(db_column='ETH', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MODULS'


class ModulsIm(models.Model):
    modul = models.FloatField(db_column='MODUL', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MODULS_IM$'


class Org(models.Model):
    orgid = models.IntegerField(db_column='OrgID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dir = models.CharField(db_column='DIR', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ORG'


class Othere(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True, db_comment='ID события')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', db_comment='Дата/время события')  # Field name made lowercase.
    cardid = models.IntegerField(db_column='CARDID', db_comment='Номер модуля')  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=60, db_comment='Собственно адемко сообщение ??')  # Field name made lowercase.
    eventtype = models.IntegerField(db_column='EventType', db_comment='Тип служебных событий')  # Field name made lowercase.
    sensorid = models.IntegerField(db_column='SensorID', db_comment='Номер датчика  - не ID зоны')  # Field name made lowercase.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    done = models.IntegerField(db_column='Done', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OTHERE'


class PacketRules(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nump = models.IntegerField(db_column='NUMP')  # Field name made lowercase.
    numadt = models.IntegerField(db_column='NUMADT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PACKET_RULES'


class Reasons(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50)  # Field name made lowercase.
    flag = models.IntegerField(db_column='FLAG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REASONS'


class RepEkc(models.Model):
    alarmid = models.IntegerField(db_column='AlarmID', primary_key=True)  # Field name made lowercase. The composite primary key (AlarmID, OP) found, that is not supported. The first column is selected.
    o_ekc = models.CharField(db_column='O_EKC', max_length=50)  # Field name made lowercase.
    reasondesc = models.CharField(db_column='ReasonDesc', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    op = models.IntegerField(db_column='OP')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REP_EKC'
        unique_together = (('alarmid', 'op'),)


class Rpersons(models.Model):
    responsibleid = models.AutoField(db_column='ResponsibleID', primary_key=True, db_comment='ID отвественного')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=60, blank=True, null=True, db_comment='Имя')  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=70, blank=True, null=True, db_comment='Отчество')  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=80, blank=True, null=True, db_comment='Фамилия')  # Field name made lowercase.
    phone = models.BigIntegerField(db_column='Phone', blank=True, null=True, db_comment='Телефон')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=110, blank=True, null=True, db_comment='Адрес')  # Field name made lowercase.
    enamobapp = models.IntegerField(db_column='EnaMobApp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RPERSONS'


class Sections(models.Model):
    sectionid = models.AutoField(db_column='SectionID', primary_key=True, db_comment='ID раздела')  # Field name made lowercase.
    cardid = models.IntegerField(db_column='CardID', db_comment='ID карточки')  # Field name made lowercase.
    sordernumber = models.IntegerField(db_column='SOrderNumber', db_comment='Логический номер раздела')  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=255, blank=True, null=True, db_comment='Примечание')  # Field name made lowercase.
    responsibleid = models.IntegerField(db_column='ResponsibleID', blank=True, null=True, db_comment='ID отвественного лица (по посл')  # Field name made lowercase.
    starttime = models.DateTimeField(db_column='StartTime', blank=True, null=True, db_comment='Старт задержки???(задержка тре')  # Field name made lowercase.
    endtime = models.DateTimeField(db_column='EndTime', blank=True, null=True, db_comment='Конец задержки??? (задержка тр')  # Field name made lowercase.
    staytime = models.DateTimeField(db_column='StayTime', blank=True, null=True, db_comment='Время до которого обеъкт долже')  # Field name made lowercase.
    npassword = models.IntegerField(db_column='NPassword', blank=True, null=True, db_comment='Цифровой пароль')  # Field name made lowercase.
    spassword = models.CharField(db_column='SPassword', max_length=50, blank=True, null=True, db_comment='Символьный пароль (кодовое сло')  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True, db_comment='Состояние раздела')  # Field name made lowercase.
    statedate = models.DateTimeField(db_column='StateDate', blank=True, null=True, db_comment='Время установки - изменения со')  # Field name made lowercase.
    sinfo = models.CharField(db_column='SInfo', max_length=255, blank=True, null=True, db_comment='Служебная информация')  # Field name made lowercase.
    startstaytime = models.DateTimeField(db_column='StartStayTime', blank=True, null=True, db_comment='Время постановки на охрану(ког')  # Field name made lowercase.
    endstaytime = models.DateTimeField(db_column='EndStayTime', blank=True, null=True, db_comment='Время постановки на охрану( ко')  # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags', db_comment='нулевой бит - охраняется разде')  # Field name made lowercase.
    monthstaytime = models.IntegerField(db_column='MonthStayTime', blank=True, null=True)  # Field name made lowercase.
    technicid = models.IntegerField(db_column='TechnicID', blank=True, null=True)  # Field name made lowercase.
    cset = models.DecimalField(db_column='CSet', max_digits=18, decimal_places=2)  # Field name made lowercase.
    cratio = models.DecimalField(db_column='CRatio', max_digits=18, decimal_places=2)  # Field name made lowercase.
    sectionname = models.CharField(db_column='SectionName', max_length=100, blank=True, null=True, db_comment='Название раздела')  # Field name made lowercase.
    invalidawaytimes = models.CharField(db_column='InvalidAwayTimes', max_length=350, blank=True, null=True)  # Field name made lowercase.
    holidays = models.CharField(db_column='Holidays', max_length=192, blank=True, null=True)  # Field name made lowercase.
    crmid = models.IntegerField(db_column='CRMID', blank=True, null=True)  # Field name made lowercase.
    crmid_2 = models.IntegerField(db_column='CRMID_2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SECTIONS'
        unique_together = (('npassword', 'sectionid'), ('cardid', 'sordernumber'), ('cardid', 'sordernumber'),)


class SectionsLog(models.Model):
    sectionid = models.IntegerField(db_column='SectionID')  # Field name made lowercase.
    cardidu = models.IntegerField(db_column='CardIDU', blank=True, null=True)  # Field name made lowercase.
    sordernumberu = models.IntegerField(db_column='SOrderNumberU', blank=True, null=True)  # Field name made lowercase.
    flagsu = models.IntegerField(db_column='FlagsU', blank=True, null=True)  # Field name made lowercase.
    cardidd = models.IntegerField(db_column='CardIDD', blank=True, null=True)  # Field name made lowercase.
    sordernumberd = models.IntegerField(db_column='SOrderNumberD', blank=True, null=True)  # Field name made lowercase.
    flagsd = models.IntegerField(db_column='FlagsD', blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    infou = models.CharField(db_column='InfoU', max_length=255, blank=True, null=True)  # Field name made lowercase.
    infod = models.CharField(db_column='InfoD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sinfou = models.CharField(db_column='SInfoU', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sinfod = models.CharField(db_column='SInfoD', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SECTIONS_LOG'


class Smsevents(models.Model):
    smsevent = models.IntegerField(db_column='SMSEvent', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SMSEvents'


class Smspers(models.Model):
    smspersonid = models.AutoField(db_column='SMSPersonID', primary_key=True, db_comment='ID пользователя SMS оповещения')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=60, blank=True, null=True, db_comment='Имя')  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=70, blank=True, null=True, db_comment='Отчество')  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=80, blank=True, null=True, db_comment='Фамилия')  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=50, db_comment='номер сотового телефона')  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=200, blank=True, null=True, db_comment='адрес')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SMSPERS'


class SprEvents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    acod = models.CharField(db_column='ACOD', unique=True, max_length=4)  # Field name made lowercase.
    cod = models.IntegerField(db_column='COD', unique=True)  # Field name made lowercase.
    def_field = models.CharField(db_column='DEF', max_length=250)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    r_acod = models.CharField(db_column='R_ACOD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    r_cod = models.IntegerField(db_column='R_COD', blank=True, null=True)  # Field name made lowercase.
    r_def = models.CharField(db_column='R_DEF', max_length=250, blank=True, null=True)  # Field name made lowercase.
    is_sensor = models.IntegerField(db_column='IS_SENSOR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPR_EVENTS'


class SprVzones(models.Model):
    zonenumber = models.IntegerField(db_column='ZoneNumber', primary_key=True)  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=50)  # Field name made lowercase.
    autocreate = models.IntegerField(db_column='AutoCreate', blank=True, null=True)  # Field name made lowercase.
    event = models.CharField(db_column='Event', max_length=4, blank=True, null=True)  # Field name made lowercase.
    section = models.IntegerField(db_column='Section', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPR_VZONES'


class Srperson(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID', db_comment='Раздел')  # Field name made lowercase.
    responsibleid = models.IntegerField(db_column='ResponsibleID', db_comment='Отвественный')  # Field name made lowercase.
    rordernumber = models.IntegerField(db_column='ROrderNumber', db_comment='Номер по порядку пользователя ')  # Field name made lowercase.
    m_event = models.IntegerField(db_column='M_EVENT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SRPERSON'
        unique_together = (('sectionid', 'rordernumber'), ('responsibleid', 'sectionid', 'rordernumber'),)


class Ssmspers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID', db_comment='ID Раздела')  # Field name made lowercase.
    smspersonid = models.IntegerField(db_column='SMSPersonID', db_comment='ID пользователя услуги SMS опо')  # Field name made lowercase.
    smsevents = models.IntegerField(db_column='SMSEvents', db_comment='событие для SMS оповещения (ви')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SSMSPERS'
        unique_together = (('smspersonid', 'sectionid'),)


class Technic(models.Model):
    technicid = models.AutoField(db_column='TechnicID', primary_key=True, db_comment='ID техника')  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=60, blank=True, null=True, db_comment='Имя')  # Field name made lowercase.
    middlename = models.CharField(db_column='MiddleName', max_length=70, blank=True, null=True, db_comment='Отчество')  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=80, blank=True, null=True, db_comment='Фамилия')  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=60, blank=True, null=True, db_comment='Примечания')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TECHNIC'


class Translit(models.Model):
    r = models.CharField(db_column='R', primary_key=True, max_length=10)  # Field name made lowercase.
    l = models.CharField(db_column='L', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Translit'


class Unittype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    info = models.CharField(db_column='INFO', unique=True, max_length=50)  # Field name made lowercase.
    lost = models.IntegerField(db_column='LOST', blank=True, null=True)  # Field name made lowercase.
    test = models.IntegerField(db_column='TEST', blank=True, null=True, db_comment='Временной интервал выхода пере')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNITTYPE'


class Unstay(models.Model):
    sectionid = models.IntegerField(db_column='SectionID', primary_key=True)  # Field name made lowercase.
    smsdone = models.IntegerField(db_column='SMSDone', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UNSTAY'


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True, db_comment='ID оператора')  # Field name made lowercase.
    username = models.CharField(db_column='UserName', unique=True, max_length=50, db_comment='Логин оператора')  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50, db_comment='Пароль оператора')  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=60, blank=True, null=True, db_comment='Информация об операторе (приме')  # Field name made lowercase.
    rights = models.IntegerField(db_column='Rights', db_comment='права оператора')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERS'


class Watche(models.Model):
    eventid = models.AutoField(db_column='EventID', primary_key=True, db_comment='ID события')  # Field name made lowercase.
    time = models.DateTimeField(db_column='Time', db_comment='Дата/время события')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', db_comment='Тип снятия или постановки на о')  # Field name made lowercase.
    responsibleid = models.IntegerField(db_column='ResponsibleID', db_comment='ID отвественного лица снявшего')  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserID', blank=True, null=True, db_comment='Код оператора')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID', db_comment='ID раздела')  # Field name made lowercase.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WATCHE'


class WeekShedule(models.Model):
    sectionid = models.IntegerField(db_column='SectionID', primary_key=True)  # Field name made lowercase. The composite primary key (SectionID, WD, START) found, that is not supported. The first column is selected.
    wd = models.IntegerField(db_column='WD')  # Field name made lowercase.
    start = models.DateTimeField(db_column='START')  # Field name made lowercase.
    end = models.DateTimeField(db_column='END')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WEEK_SHEDULE'
        unique_together = (('sectionid', 'wd', 'start'),)


class WeekSheduleLog(models.Model):
    sectionid = models.IntegerField(db_column='SectionID', blank=True, null=True)  # Field name made lowercase.
    wdu = models.IntegerField(db_column='WDU', blank=True, null=True)  # Field name made lowercase.
    startu = models.DateTimeField(db_column='STARTU', blank=True, null=True)  # Field name made lowercase.
    endu = models.DateTimeField(db_column='ENDU', blank=True, null=True)  # Field name made lowercase.
    wdd = models.IntegerField(db_column='WDD', blank=True, null=True)  # Field name made lowercase.
    startd = models.DateTimeField(db_column='STARTD', blank=True, null=True)  # Field name made lowercase.
    endd = models.DateTimeField(db_column='ENDD', blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WEEK_SHEDULE_LOG'


class Workplaces(models.Model):
    placeid = models.AutoField(db_column='PlaceID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WORKPLACES'


class Webusers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=50)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=50)  # Field name made lowercase.
    appname = models.CharField(db_column='AppName', max_length=50)  # Field name made lowercase.
    fio = models.CharField(db_column='FIO', max_length=250, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WebUsers'


class Zonekinds(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, db_comment='Вид зоны (короткозамкнутая)')  # Field name made lowercase.
    oldid = models.IntegerField(db_column='OLDID', blank=True, null=True)  # Field name made lowercase.
    ena = models.IntegerField(db_column='ENA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZONEKINDS'


class Zones(models.Model):
    zoneid = models.AutoField(db_column='ZoneID', primary_key=True, db_comment='ID зоны')  # Field name made lowercase.
    cardid = models.ForeignKey('Cards', db_column='CARDID', on_delete=models.CASCADE, db_comment='ID ОБЪЕКТА',
                               related_name='zones')  # Field name made lowercase.
    sectionid = models.ForeignKey('Sections', db_column='SectionID', on_delete=models.CASCADE, db_comment='ID раздела',
                                  related_name='sections')  # Field name made lowercase.
    zonenumber = models.IntegerField(db_column='ZoneNumber', db_comment='Логический номер зоны')  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', db_comment='Тип зоны по обслуживанию')  # Field name made lowercase.
    kind = models.IntegerField(db_column='Kind', db_comment='Тип зоны аппратный (нормально ')  # Field name made lowercase.
    eventtype = models.IntegerField(db_column='EventType', blank=True, null=True, db_comment='Тип сообщения (E307,R307 и про')  # Field name made lowercase.
    delaytime = models.IntegerField(db_column='DelayTime', db_comment='Задержка на тревогу??')  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=255, blank=True, null=True, db_comment='Описание зоны')  # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags', db_comment='Может ли зона быть в разных ра')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZONES'
        unique_together = (('sectionid', 'zonenumber', 'zoneid', 'info'),)


class ZonesLog(models.Model):
    zoneid = models.IntegerField(db_column='ZoneID', blank=True, null=True)  # Field name made lowercase.
    cardidu = models.IntegerField(db_column='CARDIDU', blank=True, null=True)  # Field name made lowercase.
    sectionidu = models.IntegerField(db_column='SectionIDU', blank=True, null=True)  # Field name made lowercase.
    zonenumberu = models.IntegerField(db_column='ZoneNumberU', blank=True, null=True)  # Field name made lowercase.
    typeu = models.IntegerField(db_column='TypeU', blank=True, null=True)  # Field name made lowercase.
    kindu = models.IntegerField(db_column='KindU', blank=True, null=True)  # Field name made lowercase.
    delaytimeu = models.IntegerField(db_column='DelayTimeU', blank=True, null=True)  # Field name made lowercase.
    flagsu = models.IntegerField(db_column='FlagsU', blank=True, null=True)  # Field name made lowercase.
    cardidd = models.IntegerField(db_column='CARDIDD', blank=True, null=True)  # Field name made lowercase.
    sectionidd = models.IntegerField(db_column='SectionIDD', blank=True, null=True)  # Field name made lowercase.
    zonenumberd = models.IntegerField(db_column='ZoneNumberD', blank=True, null=True)  # Field name made lowercase.
    typed = models.IntegerField(db_column='TypeD', blank=True, null=True)  # Field name made lowercase.
    kindd = models.IntegerField(db_column='KindD', blank=True, null=True)  # Field name made lowercase.
    delaytimed = models.IntegerField(db_column='DelayTimeD', blank=True, null=True)  # Field name made lowercase.
    flagsd = models.IntegerField(db_column='FlagsD', blank=True, null=True)  # Field name made lowercase.
    userip = models.CharField(db_column='USERIP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    op = models.CharField(db_column='OP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    infou = models.CharField(db_column='InfoU', max_length=255, blank=True, null=True)  # Field name made lowercase.
    infod = models.CharField(db_column='InfoD', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZONES_LOG'


class Zonetypes(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='ID')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, db_comment='Описание зоны')  # Field name made lowercase.
    oldid = models.IntegerField(db_column='OLDID', blank=True, null=True)  # Field name made lowercase.
    ena = models.IntegerField(db_column='ENA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ZONETYPES'


class TblAinterceptor(models.Model):
    wp = models.IntegerField(db_column='WP', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    a = models.IntegerField(db_column='A', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_AInterceptor'


class TblAlarmeE(models.Model):
    alarmid = models.IntegerField(db_column='AlarmID', primary_key=True, db_comment='ID тревоги')  # Field name made lowercase.
    zoneid = models.IntegerField(db_column='ZoneID', db_comment='ID зоны')  # Field name made lowercase.
    state = models.IntegerField(db_column='State', db_comment='Состояние тревоги')  # Field name made lowercase.
    sendtime_deg = models.DateTimeField(db_column='SendTime_Deg', blank=True, null=True, db_comment='Время отправки тревоги в ЕКЦ')  # Field name made lowercase.
    receivetime_deg = models.DateTimeField(db_column='ReceiveTime_Deg', blank=True, null=True, db_comment='Время принятия дежуркой-сервер')  # Field name made lowercase.
    confirmtime_deg = models.DateTimeField(db_column='ConfirmTime_Deg', blank=True, null=True, db_comment='Время подтверждения диспетчерм')  # Field name made lowercase.
    reason = models.IntegerField(db_column='Reason', blank=True, null=True, db_comment='Причина отработки тревоги лрно')  # Field name made lowercase.
    done = models.IntegerField(db_column='DONE', blank=True, null=True, db_comment='Флаг отработки оператором')  # Field name made lowercase.
    done_e = models.IntegerField(db_column='DONE_E', blank=True, null=True, db_comment='Флаг отработки диспетчером ЕКЦ')  # Field name made lowercase.
    receivecount = models.IntegerField(db_column='ReceiveCount', blank=True, null=True)  # Field name made lowercase.
    crew_arr = models.DateTimeField(db_column='Crew_Arr', blank=True, null=True, db_comment='Время прибытия экипажа')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_ALARME_E'


class TblAlarmBtn(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    prefix = models.CharField(db_column='PREFIX', max_length=10, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=10)  # Field name made lowercase.
    rid = models.IntegerField(db_column='RID')  # Field name made lowercase.
    zoneid = models.IntegerField(db_column='ZONEID')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_ALARM_BTN'


class TblClientCards(models.Model):
    iduser = models.IntegerField(db_column='IDUser')  # Field name made lowercase. The composite primary key (IDUser, CARDID) found, that is not supported. The first column is selected.
    cardid = models.IntegerField(db_column='CARDID')  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_CLIENT_CARDS'
        unique_together = (('iduser', 'cardid'),)


class TblDevver(models.Model):
    adt = models.IntegerField(db_column='ADT', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50)  # Field name made lowercase.
    r = models.IntegerField(db_column='R', blank=True, null=True)  # Field name made lowercase.
    im = models.IntegerField(db_column='IM', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_DevVer'


class TblEkcCall(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase. The composite primary key (ID, OName) found, that is not supported. The first column is selected.
    oname = models.CharField(db_column='OName', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_EKC_Call'
        unique_together = (('id', 'oname'),)


class TblExMech(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    card = models.IntegerField(db_column='CARD')  # Field name made lowercase.
    dry_contact = models.IntegerField(db_column='DRY_CONTACT')  # Field name made lowercase.
    type = models.IntegerField(db_column='TYPE')  # Field name made lowercase.
    num = models.IntegerField(db_column='NUM')  # Field name made lowercase.
    def_field = models.CharField(db_column='DEF', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_EX_MECH'
        unique_together = (('card', 'type', 'num', 'id', 'dry_contact', 'dt'),)


class TblEvents(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    receivetime = models.DateTimeField(db_column='ReceiveTime')  # Field name made lowercase.
    basen = models.IntegerField(db_column='BaseN')  # Field name made lowercase.
    unitn = models.IntegerField(db_column='UnitN')  # Field name made lowercase.
    eventkind = models.CharField(db_column='EventKind', max_length=10)  # Field name made lowercase.
    groupn = models.IntegerField(db_column='GroupN')  # Field name made lowercase.
    sensorn = models.IntegerField(db_column='SensorN')  # Field name made lowercase.
    workstationn = models.IntegerField(db_column='WorkstationN', blank=True, null=True)  # Field name made lowercase.
    rowver = models.TextField(db_column='RowVer', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    realtime = models.DateTimeField(db_column='RealTime', blank=True, null=True)  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_Events'


class TblGsm2SmsStat(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=20)  # Field name made lowercase.
    sms = models.CharField(db_column='SMS', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GSM2SMS_STAT'


class TblGsm2Config(models.Model):
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GSM2_CONFIG'


class TblGsm2R(models.Model):
    username = models.CharField(db_column='USERNAME', primary_key=True, max_length=20)  # Field name made lowercase.
    orgid = models.CharField(db_column='ORGID', max_length=100)  # Field name made lowercase.
    simorgid = models.IntegerField(db_column='SIMORGID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GSM2_R'


class TblGsm2R1(models.Model):
    username = models.CharField(db_column='USERNAME', primary_key=True, max_length=20)  # Field name made lowercase. The composite primary key (USERNAME, ORGID) found, that is not supported. The first column is selected.
    orgid = models.IntegerField(db_column='ORGID')  # Field name made lowercase.
    simorgid = models.IntegerField(db_column='SIMORGID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GSM2_R1'
        unique_together = (('username', 'orgid'),)


class TblGsm2Users(models.Model):
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT', blank=True, null=True)  # Field name made lowercase.
    sms = models.BinaryField(db_column='SMS')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='USERNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    appname = models.CharField(db_column='APPNAME', max_length=256, blank=True, null=True)  # Field name made lowercase.
    userhost = models.CharField(db_column='USERHOST', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GSM2_USERS'


class TblGuardR(models.Model):
    verifyid = models.CharField(db_column='VERIFYID', primary_key=True, max_length=20)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_GUARD_R'


class TblImei(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL', blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    im = models.CharField(db_column='IM', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_IMEI'


class TblLost(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    cardid = models.IntegerField(db_column='CARDID')  # Field name made lowercase.
    lastdt = models.DateTimeField(db_column='LASTDT', db_comment='дата последнего')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_LOST'


class TblLostModuls(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    modul = models.IntegerField(db_column='MODUL')  # Field name made lowercase.
    base = models.IntegerField(db_column='BASE')  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_LOST_MODULS'
        unique_together = (('modul', 'base'),)


class TblMisc(models.Model):
    eventid = models.IntegerField(db_column='EventID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_MISC'


class TblNeedModuls(models.Model):
    modul = models.IntegerField(db_column='MODUL', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_NEED_MODULS'


class TblProviders(models.Model):
    pref = models.IntegerField(db_column='PREF', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50)  # Field name made lowercase.
    color = models.IntegerField(db_column='COLOR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_PROVIDERS'


class TblRefId(models.Model):
    tbl_name = models.CharField(db_column='tbl_NAME', primary_key=True, max_length=50)  # Field name made lowercase. The composite primary key (tbl_NAME, OLD_ID) found, that is not supported. The first column is selected.
    old_id = models.IntegerField(db_column='OLD_ID')  # Field name made lowercase.
    new_id = models.IntegerField(db_column='NEW_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_REF_ID'
        unique_together = (('tbl_name', 'old_id'),)


class TblSmsnotices(models.Model):
    noticeid = models.AutoField(db_column='NoticeID', primary_key=True)  # Field name made lowercase.
    datetimewhenreceive = models.DateTimeField(db_column='DateTimeWhenReceive')  # Field name made lowercase.
    sectionid = models.IntegerField(db_column='SectionID')  # Field name made lowercase.
    crmid = models.IntegerField(db_column='CRMID', blank=True, null=True)  # Field name made lowercase.
    crmid_2 = models.IntegerField(db_column='CRMID_2', blank=True, null=True)  # Field name made lowercase.
    smspersonid = models.IntegerField(db_column='SMSPersonID')  # Field name made lowercase.
    otisnumber = models.IntegerField(db_column='OtisNumber')  # Field name made lowercase.
    npassword = models.IntegerField(db_column='NPassword')  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=13)  # Field name made lowercase.
    fio = models.CharField(db_column='FIO', max_length=150)  # Field name made lowercase.
    smskind = models.IntegerField(db_column='SMSKind')  # Field name made lowercase.
    datetimewhensent = models.DateTimeField(db_column='DateTimeWhenSent')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=1)  # Field name made lowercase.
    sms_text = models.CharField(db_column='SMS_Text', max_length=160)  # Field name made lowercase.
    sendattemptcount = models.IntegerField(db_column='SendAttemptCount', blank=True, null=True)  # Field name made lowercase.
    basenumber = models.IntegerField(db_column='BASENUMBER', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_SMSNotices'


class TblSnPhoneIm(models.Model):
    sn = models.CharField(db_column='SN', primary_key=True, max_length=20)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=10)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_SN_PHONE_IM'


class TblSprip(models.Model):
    ip = models.CharField(db_column='IP', primary_key=True, max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_SPRIP'


class TblTestZones(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dt = models.DateTimeField(db_column='DT', blank=True, null=True)  # Field name made lowercase.
    unitnumber = models.IntegerField(db_column='UNITNUMBER')  # Field name made lowercase.
    otisnumber = models.IntegerField(db_column='OTISNUMBER')  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100)  # Field name made lowercase.
    adt = models.IntegerField(db_column='ADT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_TEST_ZONES'


class TblDrycontact(models.Model):
    zoneid = models.IntegerField(db_column='ZoneID', primary_key=True)  # Field name made lowercase. The composite primary key (ZoneID, orgEventKind) found, that is not supported. The first column is selected.
    orgeventkind = models.CharField(db_column='orgEventKind', max_length=10)  # Field name made lowercase.
    neweventkind = models.CharField(db_column='newEventKind', max_length=50)  # Field name made lowercase.
    newgroupn = models.IntegerField(db_column='NewGroupN')  # Field name made lowercase.
    newsensorn = models.IntegerField(db_column='NewSensorN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbl_dryContact'
        unique_together = (('zoneid', 'orgeventkind'),)
