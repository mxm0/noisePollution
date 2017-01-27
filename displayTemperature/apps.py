from __future__ import unicode_literals
import paho.mqtt.client as paho
from django.apps import AppConfig
from django.utils import timezone


class DisplaytemperatureConfig(AppConfig):
    name = 'displayTemperature'
    verbose_name = "Displaying Temperature"
    def ready(self):
        from displayTemperature.models import Message
        def on_connect(client, userdata, flags, rc):
            print("dio can")
            print("CONNACK received with code %d." % (rc))
            client.subscribe("lora/message", qos=1)

        def on_subscribe(client, userdata, mid, granted_qos):
            print("Subscribed: "+str(mid)+" "+str(granted_qos))

        def on_message(client, userdata, msg):
            message = Message(message_text = str(msg.payload), 
                              rcv_date=timezone.now())
            message.save()
            print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
        
        client = paho.Client()
        client.username_pw_set("MassimoInnocentini", "Interject47small!Boxtrailer")
        client.on_connect = on_connect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.connect("lora-eu.iot-x.com", 3000, 60)
        client.loop_start()
        print("prova")