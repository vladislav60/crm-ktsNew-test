# Generated by Django 4.2.3 on 2024-05-23 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0002_partners_object_date_otkluchenia'),
    ]

    operations = [
        migrations.AddField(
            model_name='partners_object',
            name='sms_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='SMS кол-во номеров'),
        ),
    ]
