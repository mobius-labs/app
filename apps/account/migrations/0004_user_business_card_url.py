# Generated by Django 3.2.6 on 2021-10-13 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_business_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_card_url',
            field=models.CharField(default='a', max_length=10),
            preserve_default=False,
        ),
    ]