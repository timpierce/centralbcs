# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-14 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agist', '0002_auto_20170914_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylog',
            name='sent',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
