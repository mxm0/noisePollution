from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
import paho.mqtt.client as paho
import time
from django.shortcuts import render, redirect
from displayTemperature.models import Message, Device
from django.utils import timezone
from datetime import datetime, timedelta
from django.core import serializers
import json
from .forms import AddDeviceForm

def index(request):
    messages = Message.objects.all().order_by('rcv_date')
    template = loader.get_template('displayTemperature/index.html')
    if messages.exists():
        data = serializers.serialize("json", messages, fields=('average', 'rcv_date'))
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
        data = serializers.serialize("json", messages, fields=('average', 'rcv_date'))
        d = {}
        d['results'] = data
        d['id'] = messages.reverse()[0].id
        return JsonResponse(d)
    return HttpResponseBadRequest()

def list_device(request):
    devices = Device.objects.all()
    template = loader.get_template('displayTemperature/device_list.html')
    if devices.exists():
        context = {
            'devices': devices
        }
        return HttpResponse(template.render(context, request))
    return HttpResponseBadRequest()
    
def add_device(request):
    if request.method == "POST":
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.save()
            return redirect('list_device')
    else:
        form = AddDeviceForm()
    return render(request, 'displayTemperature/new_device.html', {'form': form})
    
