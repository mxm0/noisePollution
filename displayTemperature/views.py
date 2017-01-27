from django.http import HttpResponse
from django.template import loader
import paho.mqtt.client as paho
import time
from django.shortcuts import render, redirect
from displayTemperature.models import Message
from django.utils import timezone
from datetime import datetime, timedelta
from django.core import serializers

def index(request):
    messages = Message.objects.all().order_by('rcv_date')
    template = loader.get_template('displayTemperature/index.html')
    context = {
        'messages': messages,
        'id' : messages.reverse()[0].id
    }
    return HttpResponse(template.render(context, request))

def check_messages(request):
    last_id = request.POST['id']
    messages = Message.objects.filter(id__gt = last_id).order_by('rcv_date')
    if messages.exists():
        template = loader.get_template('displayTemperature/new_messages.html')
        context = {
            'messages': messages,
            'id' : messages.reverse()[0].id
        }
        return HttpResponse(template.render(context, request))
    return HttpResponse(status=204)
