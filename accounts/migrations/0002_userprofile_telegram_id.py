# Generated by Django 4.2.15 on 2024-09-05 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
