from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.template import loader
import paho.mqtt.client as paho
import time
from django.shortcuts import render, redirect
from displayTemperature.models import Message, Device
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.core import serializers
import json
from .forms import AddDeviceForm, EditDeviceForm, SearchDeviceForm
from googlemaps import Client

def index(request):
    return render(request, 'displayTemperature/index.html')
    
def map(request, id=None):
    return render(request, 'displayTemperature/map.html')
    
def about(request, id=None):
    return render(request,'displayTemperature/about.html')
    
def graph(request, deveui):
    print(deveui)
    messages = Message.objects.all().order_by('rcv_date')
    template = loader.get_template('displayTemperature/graph.html')
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
            api_key = "AIzaSyB0L99kRyFar3t6ecNlkyYeC7Ky14udF6o"
            gmaps = Client(api_key)
            device = form.save(commit=False)
            geocode_result = gmaps.geocode(device.address)
            device.latitude = geocode_result[0]['geometry']['location']['lat']
            device.longitude = geocode_result[0]['geometry']['location']['lng']
            device.save()
            return redirect('list_device')
    else:
        form = AddDeviceForm()
    return render(request, 'displayTemperature/new_device.html', {'form': form})

def ajax_device_search(request):
    if request.method== 'POST':
        dev_eui = request.POST.get('dev_eui')
        address = request.POST.get('address')
        device = Device(dev_eui=dev_eui, address=address)         
        results = Device.objects.filter(Q(dev_eui__contains = device) | Q(address__contains = address))
        if results.exists():
            data = serializers.serialize("json", results, fields=('dev_eui', 'address'))
            d = {}
            d['results'] = data
            return JsonResponse(d)
    else:
        form = SearchDeviceForm()
        return render(request, 'displayTemperature/device_search.html', {'form': form})
        
def edit_device(request, deveui):
    if request.method== 'POST':
        address = request.POST.get('address')
        device = Device.objects.filter(dev_eui=deveui)
        if device.exists():
            api_key = "AIzaSyB0L99kRyFar3t6ecNlkyYeC7Ky14udF6o"
            gmaps = Client(api_key)
            geocode_result = gmaps.geocode(address)
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            Device.objects.filter(dev_eui=deveui).update(address=address, latitude=latitude, longitude=longitude)
            return redirect('list_device')
    else:
        form = EditDeviceForm()
        return render(request, 'displayTemperature/edit_device.html', {'form': form})
    