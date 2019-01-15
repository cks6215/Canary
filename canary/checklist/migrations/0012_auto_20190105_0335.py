# Generated by Django 2.1.4 on 2019-01-04 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0011_auto_20181230_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 5, 3, 35, 12, 337860), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 5, 3, 35, 12, 337257), unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 5, 3, 35, 12, 337275), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 5, 3, 35, 12, 337230), unique=True),
        ),
    ]
