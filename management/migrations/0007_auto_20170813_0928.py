# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 04:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20170813_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='due_date_time',
            field=models.DateTimeField(),
        ),
    ]
