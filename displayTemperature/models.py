from __future__ import unicode_literals

from django.db import models

class Device(models.Model):
    dev_eui = models.CharField(max_length=16)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    def __int__(self):
        return self.message_value

class Message(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default = "0000000000000000")
    highest = models.IntegerField(default=0)
    average = models.IntegerField(default=0)
    lowest = models.IntegerField(default=0)
    rcv_date = models.DateTimeField()
    def __int__(self):
        return self.message_value
