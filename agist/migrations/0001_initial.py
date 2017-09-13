# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-04 01:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('age', models.PositiveSmallIntegerField()),
                ('subject', models.CharField(max_length=255)),
                ('template', models.CharField(max_length=65000)),
            ],
        ),
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when_performed', models.DateTimeField()),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agist.Action')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('indv_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('family_id', models.PositiveIntegerField(null=True)),
                ('dob', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='actionlog',
            name='indv_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agist.Member'),
        ),
    ]
