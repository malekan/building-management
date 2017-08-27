# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_auto_20170826_2338'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='options',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
