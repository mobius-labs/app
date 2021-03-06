# Generated by Django 3.2.6 on 2021-10-15 04:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_book', '0006_alter_number_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='number',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{3,15}$')]),
        ),
    ]
