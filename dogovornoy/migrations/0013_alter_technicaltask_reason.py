# Generated by Django 4.2.15 on 2024-09-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogovornoy', '0012_taskreason_technicaltask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technicaltask',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]