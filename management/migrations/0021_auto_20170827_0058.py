# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 20:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0020_auto_20170826_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='main_pic',
            field=models.FileField(default='', upload_to='unit_images'),
        ),
    ]
