# Generated by Django 3.2.6 on 2021-10-12 06:54

import apps.calendar.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='login_of_host_user',
        ),
        migrations.RemoveField(
            model_name='eventoccurrence',
            name='login_of_host_user',
        ),
        migrations.AlterField(
            model_name='event',
            name='alert',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_all_day',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='response',
            field=models.CharField(blank=True, choices=[(apps.calendar.models.EventResponse['GOI'], 'going'), (apps.calendar.models.EventResponse['TEN'], 'tentative'), (apps.calendar.models.EventResponse['DEC'], 'declined')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='tag',
            field=models.CharField(blank=True, choices=[(apps.calendar.models.EventTag['BUS'], 'business'), (apps.calendar.models.EventTag['FRN'], 'friend'), (apps.calendar.models.EventTag['FAM'], 'family'), (apps.calendar.models.EventTag['PER'], 'personal'), (apps.calendar.models.EventTag['OTH'], 'other')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
