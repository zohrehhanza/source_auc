# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-11 16:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20171211_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bid_end_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 11, 16, 55, 56, 683166)),
        ),
    ]
