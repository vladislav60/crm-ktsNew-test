# Generated by Django 4.2.3 on 2024-06-21 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0007_alter_kts_iin_bin'),
    ]

    operations = [
        migrations.AddField(
            model_name='kts',
            name='date_izmenenia',
            field=models.DateField(blank=True, null=True, verbose_name='Дата изменения'),
        ),
    ]