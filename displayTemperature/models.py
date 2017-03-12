from __future__ import unicode_literals

from django.db import models

class Message(models.Model):
    message_value = models.IntegerField(default=0)
    rcv_date = models.DateTimeField()
    def __int__(self):
        return self.message_value