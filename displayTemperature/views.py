from django.http import HttpResponse
import paho.mqtt.client as paho


def index(request):
    def on_connect(client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))
    
    def on_subscribe(client, userdata, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
    def on_message(client, userdata, msg):
        message = msg.topic+" "+str(msg.qos)+" "+str(msg.payload)
        return HttpResponse("test")  
        print(message) 
 
    client = paho.Client()
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect("broker.mqttdashboard.com", 1883)
    client.subscribe("testtopic/200", qos=1)
 
    client.loop_start()