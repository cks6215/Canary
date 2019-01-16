# Generated by Django 2.1.4 on 2019-01-16 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0013_auto_20190116_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='power',
            field=models.CharField(default='off', max_length=10),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 16, 20, 56, 58, 573307), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 16, 20, 56, 58, 571981), unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 16, 20, 56, 58, 572095), max_length=20),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 16, 20, 56, 58, 571927), unique=True),
        ),
    ]
