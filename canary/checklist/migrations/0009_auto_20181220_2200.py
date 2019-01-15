# Generated by Django 2.1.4 on 2018-12-20 13:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0008_auto_20181220_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='item_category',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checklist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 20, 22, 0, 39, 26524), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 20, 22, 0, 39, 25882), unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 20, 22, 0, 39, 25900), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 20, 22, 0, 39, 25857), unique=True),
        ),
    ]
