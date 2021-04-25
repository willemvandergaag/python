import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

import numpy as np
import cv2
import math

img = plt.imread("C:\\Users\\wille\\Desktop\\python\\map.jpg")

while True:
    xs = [100]
    ys = [100]
    print("function")
    scale = 1
    plt.imshow(img, extent=[0, 300, 0, 460])

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

    legend_elements = [Line2D([0], [0], marker='X', color='w', label='person',
                          markerfacecolor='b', markersize=15),
                    Line2D([0], [0], marker='.', color='w', label='sensor',
                          markerfacecolor='r', markersize=15)]
    
    plt.legend(handles=legend_elements, title='Symbols', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.draw()
    plt.pause(0.0001)
    plt.clf()
