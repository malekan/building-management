# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0019_auto_20170826_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.CharField(choices=[('R', 'مسکونی'), ('B', 'تجاری')], default='R', max_length=1),
        ),
    ]
