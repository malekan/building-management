# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 11:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_auto_20170813_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='main_pic',
        ),
        migrations.AddField(
            model_name='building',
            name='main_pic_src',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]