# Generated by Django 4.2.15 on 2024-11-28 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0003_invoice_alter_returnreason_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='rekvizity',
            name='img_pechat',
            field=models.ImageField(blank=True, null=True, upload_to='company_seals/', verbose_name='Печать компании'),
        ),
    ]
