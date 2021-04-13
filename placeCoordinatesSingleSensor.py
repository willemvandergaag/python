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


def placeCoordinateAlpha():
    global xs
    global ys
    xs = []
    ys = []
    alphaxImg = 24 - alphax
    xs.append(alphaxImg + 36)
    ys.append(alphay + 48)

    plt.imshow(img, extent=[0, 72, 0, 96])
    plt.plot(xs, ys, 'rX', markersize = 12)
    plt.annotate("1", # this is the text
                (xs[0],ys[0]), # this is the point to label
                textcoords="offset points", # how to position the text
                xytext=(0,10), # distance from text to points (x,y)
                ha='center') # horizontal alignment can be left, right or center
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
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    global updatedAlpha
    global updatedBeta

    if payload["sensor"] == 2:
        global alphax
        global alphay
        alphax = payload["x"]
        alphay = payload["y"]
        print("sensor 2!")
        updatedAlpha = 1
        updatedBeta = 0

        
    if updatedAlpha:
        placeCoordinateAlpha()
    
    
    


 
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










