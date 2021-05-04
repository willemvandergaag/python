import paho.mqtt.client as mqtt
import json
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
import numpy as np
import cv2
import csv
import math

from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from datetime import date


def placeCoordinates(sensors):
    fig = plt.figure()

    # display map of room
    plt.imshow(img, extent=[0, roomX, 0, roomY])

    # create heatmap of people
    createHeatmap()

    # plot locations of sensors
    plt.plot(sensorLocationX, sensorLocationY, 'r.', markersize=8)

    # If the list is not empty, plot x and y
    if(len(plotX) > 0 and len(plotY) > 0):
        plt.plot(plotX, plotY, 'bX', markersize=12)

    # display list of locations
    plt.text(-250, 445, 'Locations of people', weight='bold')

    # Offset creates a new row for every coordinate
    offsetText = 1
    # place coordinates next to map
    for i_x, i_y in zip(plotX, plotY):
        plt.text(-220, 445 - (offsetText * 20), str(offsetText) +
                 ': ' + '({}, {})'.format(i_x, i_y))
        offsetText = offsetText + 1

    # save historical data
    for i_x, i_y in zip(plotX, plotY):
        saveData(i_x, i_y)

    # legend containing symbols
    legend_elements = [Line2D([0], [0], marker='X', color='w', label='Person',
                              markerfacecolor='b', markersize=15),
                       Line2D([0], [0], marker='.', color='w', label='Sensor',
                              markerfacecolor='r', markersize=15)]

    plt.legend(handles=legend_elements, title='Symbols',
               bbox_to_anchor=(1.05, 1), loc='upper left')

    fig.canvas.draw()

    # convert image from pyplot to opencv
    cvImg = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    cvImg = cvImg.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    plt.clf()

    # img is rgb, convert to opencv's default bgr
    cvImg = cv2.cvtColor(cvImg, cv2.COLOR_RGB2BGR)

    # display image with opencv
    cv2.imshow("plot", cvImg)
    cv2.waitKey(1)


def saveData(i_x, i_y):
    # current date
    today = str(date.today())

    # create list with coordinates
    listA = []
    listA.append(i_x)
    listA.append(i_y)

    # open file and append with coordinates
    with open('C:/Users/wille/Desktop/python/historic_data/coordinates-' + today + '.csv', 'a') as myFile:
        writer = csv.writer(myFile)
        writer.writerow(listA)

    myFile.close()


def createHeatmap():
    global heatmapArray
    heatmapArray = [20] * (300 * 460)
    heatmapArray = np.asarray(heatmapArray)
    heatmapArray = heatmapArray.reshape(460, 300)

    for i in range(0, len(temps)):

        startX = round(plotX[i]) - (xSize[i] / 2)
        startY = 460 - (round(plotY[i]) + (ySize[i] / 2))

        resizeTemp = temps[i]
        resizeTemp = np.array(resizeTemp)
        resizeTemp = resizeTemp.reshape(ySize[i], xSize[i])

        resizeTemp = np.kron(resizeTemp, np.ones((4, 5)))

        resizeTemp = np.rot90(resizeTemp, 1)
        # resizeTemp = np.fliplr(resizeTemp)
        resizeTemp = np.flipud(resizeTemp)

        for x in range(0, len(resizeTemp[0]) - 1):
            for y in range(0, len(resizeTemp) - 1):
                newTemp = resizeTemp[y][x]
                heatmapArray[int(startX + x)][int(startY - y)] = newTemp

    # find min value, subtract this from all values
    minValue = math.floor(np.amin(heatmapArray))
    maxValue = math.ceil(np.amax(heatmapArray))
    heatmapComplete = heatmapArray - minValue

    # Now scaled to 0 - 255
    if minValue != maxValue:
        heatmapComplete = heatmapComplete * 255 / (maxValue - minValue)

    # apply colormap
    imgAGray = heatmapComplete.astype(np.uint8)
    imgA = cv2.applyColorMap(imgAGray, cv2.COLORMAP_JET)

    #display heatmap
    cv2.imshow('image', imgA)




def checkCoordinates():
    # Loop through all sensors
    # We finish with a list with
    # all x's and y's of all sensors
    allXY = []
    for i in range(1, numberOfSensors + 1):
        # Put all x's and y's in an object
        for j in range(0, len(sensors[i]['x'])):
            allXY.append({
                'x': sensors[i]['x'][j],
                'y': sensors[i]['y'][j],
                'xSize': sensors[i]['heatmaps'][j]['settings']['xSize'],
                'ySize': sensors[i]['heatmaps'][j]['settings']['ySize'],
                'temps':  sensors[i]['heatmaps'][j]['temps']
            })

    # Test if coordinate is close to other coordinates
    # if yes, remove
    for coordinate in allXY:
        tempAllXY = allXY.copy()
        tempAllXY.remove(coordinate)  # Remove itself
        for test_coordinaat in tempAllXY:
            if (
                (
                    test_coordinaat['x'] <= (coordinate['x'] + maxDifference) and
                    test_coordinaat['x'] >= (coordinate['x'] - maxDifference)
                ) and (
                    test_coordinaat['y'] <= (coordinate['y'] + maxDifference) and
                    test_coordinaat['y'] >= (coordinate['y'] - maxDifference)
                )
            ):
                # if there is overlap with another coordinate, remove
                allXY.remove(coordinate)

    global plotX, plotY, xSize, ySize, temps

    plotX = []
    plotY = []
    xSize = []
    ySize = []
    temps = []

    # Put in a list that plot() can handle
    for coordinate in allXY:
        plotX.append(int(coordinate['x']))
        plotY.append(int(coordinate['y']))
        xSize.append(coordinate['xSize'])
        ySize.append(coordinate['ySize'])
        temps.append(coordinate['temps'])


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("17089689")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    global stamp
    stamp = time.monotonic()
    payload = json.loads(msg.payload)
    global sensors
    data = payload['data']
    #print(payload)
    if (data['tempAlert'] > 0):
        print("Temperature above 80 detected!")

    x = []
    y = []

    heatmap = []

    for cluster in data['clusters']:
        # the location is the offset + the number of pixels - 1 * 4.8 (4.8 is the width of 1 pixel)
        x.append(sensors[data['sensor']]['offsetX'] +
                 (cluster['coordinates']['x'] - 1) * 4.8)
        # the location is the offset - the number of pixels - 1 * 3.5 (3.5 is the width of 1 pixel)
        y.append(sensors[data['sensor']]['offsetY'] -
                 (cluster['coordinates']['y'] - 1) * 3.5)

        heatmap = cluster['heatmaps']

    # Add data to dictionary of sensor
    sensors[data['sensor']]['x'] = x
    sensors[data['sensor']]['y'] = y
    sensors[data['sensor']]['humans'] = data['humans']
    sensors[data['sensor']]['heatmaps'] = heatmap

    #check overlaying coordinates
    checkCoordinates()

    placeCoordinates(sensors)


def readConfig():
    # Read config file
    f = open("C:\\Users\\wille\\Desktop\\python\\config.json")
    data = json.load(f)
    # Read room size
    global roomX
    global roomY
    roomX = data['Room width']
    roomY = data['Room length']
    # Read number of sensors
    global numberOfSensors
    numberOfSensors = data['Number of sensors']

    # numberOfSensors = 2
    global sensorLocationX
    global sensorLocationY

    sensorLocationX = []
    sensorLocationY = []

    for i in range(1, numberOfSensors + 1):
        # read sensor locations
        locationX = data['locations'][i - 1]['x']
        locationY = data['locations'][i - 1]['y']

        sensorLocationX.append(locationX)
        sensorLocationY.append(locationY)

        # offset is to sensor, coordinates start at the top left of a sensor
        # The field visible to the sensor is 1.56 x 0.84
        # the center of the first pixel is 75.6 to the left an 40.75 to the top
        offsetX = locationX - 75.6
        offsetY = locationY + 40.75
        sensors[i] = {
            'offsetX': offsetX,
            'offsetY': offsetY,
            'x': [],
            'y': [],
            'humans': 0,
            'heatmaps': []
        }

        f.close()


sensors = {}
maxDifference = 30.0

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# read config file
readConfig()

client.connect("192.168.0.107", 1883)
img = plt.imread("C:\\Users\\wille\\Desktop\\python\\maptoscale.jpg")
img = cv2.resize(img, (300, 460))

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()
# 300 x 460
