import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation


import numpy as np
import cv2
import math

img = plt.imread("C:\\Users\\wille\\Desktop\\python\\map.jpg")

while True:
    xs = [120]
    ys = [150]
    print("function")

    plt.imshow(img, extent=[0, 240, 0, 320])

    plt.plot(xs, ys, 'rX', markersize=12)

    for x,y in zip(xs,ys):
        label = f"({x},{y})"

        plt.annotate(label, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    # plt.xlim([0, 24])
    # plt.ylim([0, 32])
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
