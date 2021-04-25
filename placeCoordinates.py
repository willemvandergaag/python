import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

sensors = {}
maxDifference = 30.0

def placeCoordinates(sensors):
    plt.imshow(img, extent=[0, roomX, 0, roomY])

    checkCoordinates()    
    
    plt.plot(sensorLocationX, sensorLocationY, 'r.', markersize = 8)

    # If the list is not empty, plot x and y
    if(len(plotX) > 0 and len(plotY) > 0):
        plt.plot(plotX, plotY, 'bX', markersize = 12)

    for i_x, i_y in zip(plotX, plotY):
        plt.text(i_x, i_y, '({}, {})'.format(i_x, i_y))

    # legend containing symbols
    legend_elements = [Line2D([0], [0], marker='X', color='w', label='Person',
                        markerfacecolor='b', markersize=15),
                    Line2D([0], [0], marker='.', color='w', label='Sensor',
                            markerfacecolor='r', markersize=15)]
    
    plt.legend(handles=legend_elements, title='Symbols', bbox_to_anchor=(1.05, 1), loc='upper left')
        
    plt.draw()
    plt.pause(0.0001)
    plt.clf()

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
                'y': sensors[i]['y'][j]
            })

    # Test if coordinate is close to other coordinates
    # if yes, remove
    for coordinate in allXY:
        tempAllXY = allXY.copy()
        tempAllXY.remove(coordinate) # Remove itself
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

    global plotX, plotY

    plotX = []
    plotY = []

    # Put in a list that plot() can handle
    for coordinate in allXY:
        plotX.append(round(coordinate['x'], 1))
        plotY.append(round(coordinate['y'], 1))

        # if len(plotX) > 1 :
    #     print(allXY)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("17089689")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    global sensors
    data = payload['data']
    #print(payload)
    if (data['tempAlert'] > 0):
        print("Temperature above 80 detected!")

    x = []
    y = []

    for cluster in data['clusters']:
        # the location is the offset + the number of pixels - 1 * 4.8 (4.8 is the width of 1 pixel)
        x.append(sensors[data['sensor']]['offsetX'] + (cluster['x'] - 1) * 4.8)
        # the location is the offset - the number of pixels - 1 * 3.5 (3.5 is the width of 1 pixel)
        y.append(sensors[data['sensor']]['offsetY'] - (cluster['y'] - 1) * 3.5)

    # Add data to dictionary of sensor
    sensors[data['sensor']]['x'] = x
    sensors[data['sensor']]['y'] = y
    sensors[data['sensor']]['humans'] = data['humans']

    placeCoordinates(sensors)
 
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

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
        'offsetX' : offsetX,
        'offsetY' : offsetY,
        'x' : [],
        'y' : [],
        'humans' : 0
    }

    f.close()

client.connect("192.168.0.107", 1883)
img = plt.imread("C:\\Users\\wille\\Desktop\\python\\maptoscale.jpg")
 
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()
# 300 x 460