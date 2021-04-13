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

iterationsAlphaX = 0
iterationsBetaX = 0
iterationsAlphaY = 0
iterationsBetaY = 0

alpha = ''
beta = ''

distanceY = 0
 
def calculate_distance():
    global iterationsAlphaX
    global iterationsBetaX
    global iterationsAlphaY
    global iterationsBetaY
    global distanceY

    # distanceX = int(input("Distance between 2 sensors in cm: "))
    distanceX = 110
    distanceY = -2

    if distanceY == 1:
        iterationsAlphaY = 23
        iterationsBetaY = 1
    elif distanceY == 2:
        iterationsAlphaY = 22
        iterationsBetaY = 2
    elif distanceY == 3:
        iterationsAlphaY = 21
        iterationsBetaY = 3
    elif distanceY == 4:
        iterationsAlphaY = 20
        iterationsBetaY = 4
    elif distanceY == -1:
        iterationsAlphaY = 1
        iterationsBetaY = 23
    elif distanceY == -2:
        iterationsAlphaY = 2
        iterationsBetaY = 22
    elif distanceY == -3:
        iterationsAlphaY = 3
        iterationsBetaY = 21
    elif distanceY == -4:
        iterationsAlphaY = 4
        iterationsBetaY = 20

    if distanceX >= 70 and distanceX < 80:
        iterationsAlphaX = 26
        iterationsBetaX = 4
    elif distanceX >= 80 and distanceX < 100:
        iterationsAlphaX = 29
        iterationsBetaX = 2
    elif distanceX >= 100 and distanceX < 120:
        iterationsAlphaX = 30
        iterationsBetaX = 1
    elif distanceX >= 120:
        iterationsAlphaX = 31
        iterationsBetaX = 0
    elif distanceX > 140:
        print("Sensors too far apart!")
        exit()


def combine_images():
    if alpha and beta:
        A = np.matrix(alpha)
        B = np.matrix(beta)

        outputA = A.reshape(24,32)
        outputB = B.reshape(24,32)
        outputC = A.reshape(24,32)
        outputD = B.reshape(24,32)

        iterationsListAlphaX = list(range(iterationsAlphaX, 32))
        iterationsListBetaX = list(range(0, iterationsBetaX))

        
        # print(iterationsAlphaY, iterationsBetaY)
        # print(iterationsListAlphaY, iterationsListBetaY)

        outputC = np.delete(outputC, iterationsListAlphaX, 1)
        outputD = np.delete(outputD, iterationsListBetaX, 1)

        if distanceY > 0:
            iterationsListAlphaY = list(range(iterationsAlphaY, 24))
            iterationsListBetaY = list(range(0, iterationsBetaY))
            print(iterationsListAlphaY, iterationsListBetaY)
            outputC = np.delete(outputC, iterationsListAlphaY, 0)
            outputD = np.delete(outputD, iterationsListBetaY, 0)
        
        if distanceY < 0:
            iterationsListBetaY = list(range(iterationsBetaY, 24))
            iterationsListAlphaY = list(range(0, iterationsAlphaY))
            print(iterationsListAlphaY, iterationsListBetaY)
            outputC = np.delete(outputC, iterationsListAlphaY, 0)
            outputD = np.delete(outputD, iterationsListBetaY, 0)

        ###################

        outputE = np.append(outputC, outputD, axis=1)
        num_rows, num_cols = outputE.shape

        # create colormap
        minValue = math.floor(np.amin(outputE))
        maxValue = math.ceil(np.amax(outputE))
        outputEE = outputE - minValue      
        outputEE = outputEE * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

        # resize image
        num_cols = num_cols * 10
        num_rows = num_rows * 10
        dim = (num_cols, num_rows)
        outputEE = cv2.resize(outputEE, dim, interpolation = cv2.INTER_LINEAR )

        # apply colormap
        imgEGray = outputEE.astype(np.uint8)
        imgE = cv2.applyColorMap(imgEGray, cv2.COLORMAP_JET)

        cv2.imshow("merged with cutting", imgE)
        cv2.imwrite("C:/Users/wille/Desktop/python/merged_with_cuttin.jpg", imgE)
       

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
        cv2.imwrite("C:/Users/wille/Desktop/python/merged_with_cutting.jpg", imgD)

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
        cv2.imwrite("C:/Users/wille/Desktop/python/Original_B.jpg", imgB)
        cv2.imwrite("C:/Users/wille/Desktop/python/Original_A.jpg", imgA)

        cv2.waitKey(0)

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

    elif payload["sensor"] == 1:
        print("sensor 2!")
        global beta
        beta = payload["temperatures"]

    if alpha and beta:
        calculate_distance()
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

