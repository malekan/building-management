# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 04:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20170813_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='due_date_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 20, 4, 31, 52, 380419, tzinfo=utc)),
        ),
    ]