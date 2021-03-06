# Generated by Django 2.1.4 on 2019-01-18 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0014_auto_20190116_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 18, 22, 23, 41, 209814), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 18, 22, 23, 41, 209132), unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 18, 22, 23, 41, 209188), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 18, 22, 23, 41, 209104), unique=True),
        ),
    ]
