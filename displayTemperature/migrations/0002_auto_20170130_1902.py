# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-30 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displayTemperature', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='rcv_date',
            field=models.DateTimeField(),
        ),
    ]
