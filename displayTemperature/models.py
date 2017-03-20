from __future__ import unicode_literals

from django.db import models

class Device(models.Model):
    dev_eui = models.CharField(max_length=16)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    lowest = models.FloatField(default=0)
    highest = models.FloatField(default=0)
    def __str__(self):
        return self.dev_eui

class Message(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default = "0000000000000000")
    average = models.FloatField(default=0)
    rcv_date = models.DateTimeField()
    def __int__(self):
        return self.average
