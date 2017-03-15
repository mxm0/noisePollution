from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
import paho.mqtt.client as paho
import time
from django.shortcuts import render, redirect
from displayTemperature.models import Message
from django.utils import timezone
from datetime import datetime, timedelta
from django.core import serializers
import json


def index(request):
    messages = Message.objects.all().order_by('rcv_date')
    template = loader.get_template('displayTemperature/index.html')
    if messages.exists():
        data = serializers.serialize("json", messages, fields=('message_value', 'rcv_date'))
        context = {
            'messages': data,
            'id' : messages.reverse()[0].id
        }
        return HttpResponse(template.render(context, request))
    return HttpResponseBadRequest()

def check_messages(request):
    last_id = request.POST['id']
    messages = Message.objects.filter(id__gt = last_id).order_by('rcv_date')
    if messages.exists():
        data = serializers.serialize("json", messages, fields=('message_value', 'rcv_date'))
        d = {}
        d['results'] = data
        d['id'] = messages.reverse()[0].id
        return JsonResponse(d)
    return HttpResponseBadRequest()

def add_device(request):
    