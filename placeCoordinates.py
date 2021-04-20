import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
sensors = {}

def placeCoordinates(sensors):

    plt.imshow(img, extent=[0, roomX, 0, roomY])
    for i in range(1, numberOfSensors + 1):
        if sensors[i]['humans'] > 0:
            x = sensors[i]['x'] * 3.5 + sensors[i]['offsetX']
            y = sensors[i]['y'] * 4.8 + sensors[i]['offsetY']
            plt.plot(x, y, 'rX', markersize = 12)
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

    sensors[data['sensor']]['x'] = x
    sensors[data['sensor']]['y'] = y
    sensors[data['sensor']]['humans'] = data['humans']

    print(sensors)

    placeCoordinates(sensors)
 
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

global roomX
global roomY
roomX = int(input("Width of room in cm: "))
roomY = int(input("Length of room in cm: "))

global numberOfSensors
numberOfSensors = int(input("Number of sensors? "))

for i in range(1, numberOfSensors + 1):
    offsetX = int(input("X-offset sensor "+ str(i) + " in cm: "))
    offsetY = int(input("Y-offset sensor "+ str(i) + " in cm: "))
    sensors[i] = {
        'offsetX' : offsetX,
        'offsetY' : offsetY
    }

client.connect("192.168.0.107", 1883)
img = plt.imread("C:\\Users\\wille\\Desktop\\python\\map.jpg")
 
# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()
# 300 x 460