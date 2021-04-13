# MQTT Client demo
# Continuously monitor two different MQTT topics for data,
# check if the received data matches two predefined 'commands'
 
import paho.mqtt.client as mqtt
import json

import numpy as np
import cv2, math

scaling = 10

width = scaling * 32
height = scaling * 24

alpha = ""
beta = ""
iterationsAlpha = 0
iterationsBeta = 0
distanceY = 0
updatedAlpha = 0
updatedBeta = 0
 
def calculate_distance():
    global iterationsAlpha
    global iterationsBeta
    global distanceY

    distanceY = int(input("Distance between 2 sensors in cm: "))
    if distanceY >= 70 and distanceY < 80:
        iterationsAlpha = 28
        iterationsBeta = 2
    elif distanceY >= 80 and distanceY < 100:
        iterationsAlpha = 28
        iterationsBeta = 2
    elif distanceY >= 100 and distanceY < 120:
        iterationsAlpha = 29
        iterationsBeta = 1
    elif distanceY >= 120:
        iterationsAlpha = 30
        iterationsBeta = 0
    elif distanceY > 140:
        print("Sensors too far apart!")
        exit()


    #distanceX = input("Offset between sensors in cm")


def combine_images():
    if alpha and beta:
        A = np.matrix(alpha)
        B = np.matrix(beta)
        updatedAlpha = 0
        updatedBeta = 0
        print(updatedAlpha)
        print(updatedBeta)

        outputA = A.reshape(24,32)
        outputB = B.reshape(24,32)
        outputC = A.reshape(24,32)
        outputD = B.reshape(24,32)

        iterationsListAlpha = list(range(iterationsAlpha + 1, 32))
        #print(iterationsListAlpha)

        iterationsListBeta = list(range(0, iterationsBeta))
        #print(iterationsListBeta)

        outputC = np.delete(outputC, iterationsListAlpha, 1)
        outputD = np.delete(outputD, iterationsListBeta, 1)

        outputE = np.append(outputC, outputD, axis=1)

        np.savetxt("data.csv", outputE, delimiter = ",")

        print("File updated!")
    
        



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("17089689")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)

    if payload["sensor"] == 2:
        global alpha
        alpha = payload["temperatures"]
        print("sensor 1!")
        global updatedAlpha
        updatedAlpha = 1

    elif payload["sensor"] == 1:
        print("sensor 2!")
        global beta
        beta = payload["temperatures"]
        global updatedBeta
        updatedBeta = 1

    global distanceY

    if alpha and beta and not distanceY:
        calculate_distance()
        
    elif updatedBeta and updatedAlpha and distanceY:
        combine_images()


 
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("192.168.0.107", 1883)
 
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()

