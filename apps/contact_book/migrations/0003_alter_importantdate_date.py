# Generated by Django 3.2.6 on 2021-10-01 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_book', '0002_alter_importantdate_important_date_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importantdate',
            name='date',
            field=models.DateField(),
        ),
    ]
