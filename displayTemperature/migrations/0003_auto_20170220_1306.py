# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-20 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('displayTemperature', '0002_auto_20170130_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_text',
        ),
        migrations.AddField(
            model_name='message',
            name='message_value',
            field=models.IntegerField(default=0),
        ),
    ]
