# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-16 05:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loglan', '0012_auto_20170413_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='useractivationkey',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2017, 4, 16)),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
