# Generated by Django 3.2.6 on 2021-10-13 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_connected_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_card',
            field=models.BooleanField(default=False),
        ),
    ]