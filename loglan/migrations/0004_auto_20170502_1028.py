# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-02 03:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loglan', '0003_auto_20170429_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalscore',
            name='user',
        ),
        migrations.AlterField(
            model_name='coursepart',
            name='course_part_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='useractivationkey',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 5, 2)),
        ),
        migrations.DeleteModel(
            name='TotalScore',
        ),
    ]
