# Generated by Django 4.2.3 on 2024-06-05 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0006_alter_partners_object_tariff_per_mounth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kts',
            name='iin_bin',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ИИН/БИН'),
        ),
    ]