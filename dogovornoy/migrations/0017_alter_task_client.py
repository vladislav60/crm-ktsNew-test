# Generated by Django 4.2.15 on 2024-10-03 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0016_partners_object_prochee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dogovornoy.kts', verbose_name='id клиента из ктс'),
        ),
    ]