# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-17 17:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('f2fsignup', '0004_auto_20170917_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='dow_first_choice',
        ),
        migrations.RemoveField(
            model_name='member',
            name='dow_second_choice',
        ),
    ]
