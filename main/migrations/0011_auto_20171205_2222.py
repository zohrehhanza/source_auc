# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-06 03:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20171205_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bid_end_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 5, 22, 32, 14, 694771)),
        ),
    ]