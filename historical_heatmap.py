import csv
import math
import numpy as np
import cv2
import cv2
import os
import sys

roomWidth = 300
roomLength = 460
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
                    # add 1 to the location of the coordinates
                    a = int(row[0])
                    b = int(row[1])
                    heatmapArray[roomLength - b][a] += 1

heatmap = heatmapArray


# find min value, subtract this from all values
minValue = math.floor(np.amin(heatmap))
maxValue = math.ceil(np.amax(heatmap))
print(minValue)
print(maxValue)
heatmapComplete = heatmap - minValue

# Now scaled to 0 - 255
heatmapComplete = heatmapComplete * 255 / (maxValue - minValue)

# apply colormap
imgAGray = heatmapComplete.astype(np.uint8)
imgA = cv2.applyColorMap(imgAGray, cv2.COLORMAP_JET)

# resize map to size of heatmap
imgMap = cv2.resize(imgMap, (roomWidth, roomLength))

# blend both images
dst = cv2.addWeighted(imgMap, 0.6, imgA, 0.4, 0)

#display heatmap over map
cv2.imshow('Historic heatmap', imgA)

cv2.waitKey(0)