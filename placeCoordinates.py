import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
sensors = {}
maxDifference = 30.0

def placeCoordinates(sensors):
    plt.imshow(img, extent=[0, roomX, 0, roomY])
    all_xy = []
    # Loop door alle sensoren heen
    # We eindigen uiteindelijk met een grote lijst met
    # alle x en y's van alle sensoren in variable all_xy
    for i in range(1, numberOfSensors + 1):
        # Zet alle bijbehorende x en y's in een object
        for j in range(0, len(sensors[i]['x'])):
            all_xy.append({
                'x': sensors[i]['x'][j],
                'y': sensors[i]['y'][j]
            })

    # Test of een van de andere coordinaten teveel op deze lijkt
    # zo ja, gooi zichzelf eruit
    for coordinaat in all_xy:
        temp_all_xy = all_xy.copy()
        temp_all_xy.remove(coordinaat) # Verwijder zichzelf
        for test_coordinaat in temp_all_xy:
            if (
                (
                    test_coordinaat['x'] <= (coordinaat['x'] + maxDifference) and
                    test_coordinaat['x'] >= (coordinaat['x'] - maxDifference)
                ) and (
                    test_coordinaat['y'] <= (coordinaat['y'] + maxDifference) and
                    test_coordinaat['y'] >= (coordinaat['y'] - maxDifference)
                )
            ):
                # print(all_xy)
                # print(coordinaat)
                all_xy.remove(coordinaat)
    
    plotX = []
    plotY = []

    
    # Ga weer terug naar een list waar plot() mee om kan gaan
    for coordinaat in all_xy:
        plotX.append(coordinaat['x'])
        plotY.append(coordinaat['y'])

    if len(plotX) > 1 :
        print(all_xy)
    # Als de list niet leeg is, plot dan x en y
    if(len(plotX) > 0 and len(plotY) > 0):
        plt.plot(plotX, plotY, 'rX', markersize = 12)

    plt.draw()
    plt.pause(0.0001)
    plt.clf()
    updatedAlpha = 0

def filterCoordinates(coordinate, x, y, maxDifference):
    if (
        (coordinate['x'] <= (x + maxDifference) and coordinate['x'] >= (x - maxDifference)) and
        (coordinate['y'] <= (y + maxDifference) and coordinate['y'] >= (y - maxDifference))
    ):
        return False
    else:
        return True

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

global roomX
global roomY
# roomX = int(input("Width of room in cm: "))
# roomY = int(input("Length of room in cm: "))
roomX = 300
roomY = 460

global numberOfSensors
# numberOfSensors = int(input("Number of sensors? "))

numberOfSensors = 2

for i in range(1, numberOfSensors + 1):
    offsetX = int(input("X-offset sensor " + str(i) + " in cm: "))
    offsetY = int(input("Y-offset sensor " + str(i) + " in cm: "))
    # offset is to sensor, coordinates start at the top left of a sensor
    # The field visible to the sensor is 1.56 x 0.84
    # the center of the first pixel is 75.6 to the left an 40.75 to the top
    offsetX = offsetX - 75.6
    offsetY = offsetY + 40.75
    sensors[i] = {
        'offsetX' : offsetX,
        'offsetY' : offsetY,
        'x' : [],
        'y' : [],
        'humans' : 0
    }

client.connect("192.168.0.107", 1883)
img = plt.imread("C:\\Users\\wille\\Desktop\\python\\maptoscale.jpg")
 
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()
# 300 x 460