import csv
import math
import numpy as np
import cv2
import cv2
import os
import sys
import json

# Read config file
f = open("C:\\Users\\wille\\Desktop\\python\\configHistory.json")
data = json.load(f)
# Read room size
roomWidth = data['Room width']
roomLength = data['Room length']
# Read diameter person
diameterPerson = data['Width person(pixels)']

# Create array for heatmap and resize
heatmapArray = [0] * (roomLength * roomWidth)
heatmapArray = np.asarray(heatmapArray)
heatmapArray = heatmapArray.reshape(roomLength, roomWidth)

# location of heatmaps
path = "C:/Users/wille/Desktop/python/historic_data"

# location of map
imgMap = cv2.imread("C:\\Users\\wille\\Desktop\\python\\maptoscale.jpg")
filelist = []

for root, dirs, files in os.walk(path):
    # get the names of all files
	for file in files:
        #append the file name to the list
		filelist.append(os.path.join(root,file))

for name in filelist:
    # go through every file
    with open(name) as csv_file:
        # read in file
            csv_reader = csv.reader(csv_file, delimiter=',')
            #  only if there is something on a row
            for row in csv_reader:
                if row:
                    # get coordinates
                    a = int(row[0])
                    b = int(row[1])
                    radiusPerson = round(diameterPerson / 2)
                    # place radius around person
                    for x in range (a - radiusPerson, a + radiusPerson):
                        for y in range (b - radiusPerson, b + radiusPerson):
                            heatmapArray[roomLength - y][x] += 1

# find min value, subtract this from all values
minValue = math.floor(np.amin(heatmapArray))
maxValue = math.ceil(np.amax(heatmapArray))
heatmapComplete = heatmapArray - minValue

# Now scaled to 0 - 255
heatmapComplete = heatmapComplete * 255 / (maxValue - minValue)

# apply colormap
imgAGray = heatmapComplete.astype(np.uint8)
imgA = cv2.applyColorMap(imgAGray, cv2.COLORMAP_JET)

# resize map to size of heatmap
imgMap = cv2.resize(imgMap, (roomWidth, roomLength))

# blend both images
dst = cv2.addWeighted(imgMap, 0.25, imgA, 0.75, 0)

#display heatmap over map
cv2.imshow('Historic heatmap', dst)

cv2.waitKey(0)