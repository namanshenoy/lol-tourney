# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-26 07:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20170226_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(verbose_name=datetime.datetime(2017, 2, 26, 7, 58, 53, 890919)),
        ),
    ]
