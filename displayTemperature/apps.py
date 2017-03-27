from __future__ import unicode_literals
import paho.mqtt.client as paho
from django.apps import AppConfig
from django.utils import timezone
import json
import base64


class DisplaytemperatureConfig(AppConfig):
    name='displayTemperature'
    verbose_name="Displaying Temperature"
    def ready(self):
        from displayTemperature.models import Message, Device
        def on_connect(client, userdata, flags, rc):
            print("CONNACK received with code %d." % (rc))
            client.subscribe("/lora/008000000000be50/message", qos=1)

        def on_subscribe(client, userdata, mid, granted_qos):
            print("Subscribed: "+str(mid)+" "+str(granted_qos))

        def on_message(client, userdata, msg):
            response = json.loads(msg.payload)
            decoded_data = base64.b64decode(response['data']).decode("utf-8").split("-")
            print("Message received")
            print(decoded_data)
            highest = decoded_data[0]
            average = decoded_data[1]
            lowest = decoded_data[2]
            device = Device.objects.filter(dev_eui=response['dev_eui']).first()
            if device is not None:
                message = Message(average=average, 
                                  rcv_date=timezone.now(),
                                  device=device)
                device.highest = highest
                device.lowest = lowest
                device.save()
                message.save()
            
        def on_log(mqttc, obj, level, string):
            print(string)
        
        client=paho.Client(transport="websockets")
        client.username_pw_set(username="MassimoInnocentini", password="Interject47small!Boxtrailer")
        client.on_connect=on_connect
        client.on_subscribe=on_subscribe
        client.on_message=on_message
        client.on_log=on_log
        client.connect("lora-eu.iot-x.com", 3000, 60)
        client.loop_start()

