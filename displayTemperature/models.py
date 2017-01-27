from __future__ import unicode_literals

from django.db import models

class Message(models.Model):
    message_text = models.CharField(max_length=200)
    rcv_date = models.DateTimeField()
    def __str__(self):
        return self.message_text