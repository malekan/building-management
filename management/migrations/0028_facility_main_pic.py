# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-27 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0027_auto_20170827_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='main_pic',
            field=models.FileField(default='../../../static/facility_default.png', upload_to='unit_images'),
        ),
    ]