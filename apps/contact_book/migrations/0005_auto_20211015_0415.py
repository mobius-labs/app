# Generated by Django 3.2.6 on 2021-10-15 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_book', '0004_auto_20211011_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email_address',
            field=models.EmailField(max_length=45),
        ),
        migrations.AlterField(
            model_name='number',
            name='number',
            field=models.CharField(max_length=15),
        ),
    ]