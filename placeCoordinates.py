import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation


import numpy as np
import cv2, math

alphax = 0
alphay = 0
betax = 0
betay = 0
xs = []
ys = []


def placeCoordinates(sensors):
    alphaxImg = 24 - alphax
    xs.append(alphaxImg + 36)
    ys.append(alphay + 48)

    plt.imshow(img, extent=[0, 72, 0, 96])
    for i in sensors:
        plt.plot(sensors[i]['x'], sensors[i]['y'], 'rX', markersize = 12)
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
    updatedAlpha = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("17089689")

sensors = {}

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    global sensors
    data = payload['data']
    print(payload)
    if (data['tempAlert'] > 0):
        print("Temperature above 80 detected!")

    # if(data['humans']):
    x = []
    y = []
    for cluster in data['clusters']:
        x.append(cluster['x'])
        y.append(cluster['y'])
    sensors[data['sensor']] = {
        'x': x,
        'y': y,
        'humans': data['humans']
        }

    placeCoordinates(sensors)
 
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect("192.168.0.107", 1883)
img = plt.imread("C:\\Users\\wille\\Desktop\\python\\map.jpg")
 
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()