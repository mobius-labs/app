# Generated by Django 3.2.6 on 2021-10-13 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_business_card_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='business_card_url',
        ),
    ]
