# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0034_unit_number_of_residents'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_manager',
            field=models.BooleanField(default=True),
        ),
    ]
