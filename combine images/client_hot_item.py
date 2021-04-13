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

def combine_images():
    if alpha and beta:
        A = np.matrix(alpha)
        B = np.matrix(beta)

        outputA = A.reshape(24,32)
        outputB = B.reshape(24,32)
        outputC = A.reshape(24,32)
        outputD = B.reshape(24,32)

        iterationsListAlpha = list(range(iterationsAlpha + 1, 32))
        print(iterationsListAlpha)

        iterationsListBeta = list(range(0, iterationsBeta))
        print(iterationsListBeta)

        outputC = np.delete(outputC, iterationsListAlpha, 1)
        outputD = np.delete(outputD, iterationsListBeta, 1)

        ###################

        outputE = np.append(outputC, outputD, axis=1)
        num_rows, num_cols = outputE.shape


        minValue = math.floor(np.amin(outputE))
        maxValue = math.ceil(np.amax(outputE))
        outputEE = outputE - minValue      
        outputEE = outputEE * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        num_cols = num_cols * 10
        dim = (num_cols, height)
        outputEE = cv2.resize(outputEE, dim, interpolation = cv2.INTER_LINEAR )

        # apply colormap
        imgEGray = outputEE.astype(np.uint8)
        imgE = cv2.applyColorMap(imgEGray, cv2.COLORMAP_JET)

        cv2.imshow("merged with cutting", imgE)

        ###########################
        outputD = np.append(outputA, outputB, axis=1)

        minValue = math.floor(np.amin(outputD))
        maxValue = math.ceil(np.amax(outputD))
        outputD = outputD - minValue      
        outputD = outputD * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        dim = (width * 2, height)
        outputD = cv2.resize(outputD, dim, interpolation = cv2.INTER_LINEAR )

        # apply colormap
        imgDGray = outputD.astype(np.uint8)
        imgD = cv2.applyColorMap(imgDGray, cv2.COLORMAP_JET)

        winname = "merged without cutting"
        cv2.namedWindow(winname)        # Create a named window
        cv2.moveWindow(winname, 40,30)  # Move it to (40,30)
        cv2.imshow(winname, imgD)

        #############################

        minValue = math.floor(np.amin(outputB))
        maxValue = math.ceil(np.amax(outputB))
        outputBB = outputB - minValue      
        outputBB = outputBB * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        dim = (width, height)
        outputBB = cv2.resize(outputBB, dim, interpolation = cv2.INTER_LINEAR )

        # apply colormap
        imgBGray = outputBB.astype(np.uint8)
        imgB = cv2.applyColorMap(imgBGray, cv2.COLORMAP_JET)

        # ####################

        minValue = math.floor(np.amin(outputA))
        maxValue = math.ceil(np.amax(outputA))
        outputAA = outputA - minValue      
        outputAA = outputAA * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        dim = (width, height)
        outputAA = cv2.resize(outputAA, dim, interpolation = cv2.INTER_LINEAR )

        # apply colormap
        imgAGray = outputAA.astype(np.uint8)
        imgA = cv2.applyColorMap(imgAGray, cv2.COLORMAP_JET)

        #########################

        cv2.imshow("Original B", imgB)
        cv2.imshow("Original A", imgA)

        cv2.waitKey(0)
 
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("17089689")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    combine_images()
    payload = json.loads(msg.payload)

    if payload["sensor"] == 2:
        global alpha
        alpha = payload["temperatures"]
        global iterationsAlpha
        print("sensor 1!")
        iterationsAlpha = payload["x"]
        print(payload["x"])

    elif payload["sensor"] == 1:
        print("sensor B!")
        global beta
        beta = payload["temperatures"]
        global iterationsBeta
        iterationsBeta = payload["x"]
        print(payload["x"])

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

