# Generated by Django 2.1.4 on 2019-01-23 07:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0015_auto_20190118_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 16, 24, 29, 786802), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 16, 24, 29, 786118), unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 16, 24, 29, 786175), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 23, 16, 24, 29, 786091), unique=True),
        ),
    ]
