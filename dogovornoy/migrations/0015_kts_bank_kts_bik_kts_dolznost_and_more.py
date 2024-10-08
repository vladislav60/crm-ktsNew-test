# Generated by Django 4.2.15 on 2024-09-27 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0014_technicaltask_ekcbase_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='kts',
            name='bank',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='БАНК'),
        ),
        migrations.AddField(
            model_name='kts',
            name='bik',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='БИК'),
        ),
        migrations.AddField(
            model_name='kts',
            name='dolznost',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Должность директора'),
        ),
        migrations.AddField(
            model_name='kts',
            name='fio_direktor_polnoe',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя директора полное'),
        ),
        migrations.AddField(
            model_name='kts',
            name='fio_direktor_sokr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя директора сокращенное'),
        ),
        migrations.AddField(
            model_name='kts',
            name='iik',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ИИК'),
        ),
        migrations.AddField(
            model_name='kts',
            name='rezhim_raboti',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Режим работы'),
        ),
        migrations.AddField(
            model_name='kts',
            name='ucereditel_doc',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Учередительные документы'),
        ),
    ]
