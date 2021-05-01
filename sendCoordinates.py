from numpy import loadtxt

from pylab import *
from scipy.ndimage import measurements
from scipy import ndimage
import math
import time
import board
import busio
import adafruit_mlx90640
import paho.mqtt.publish as publish
import json

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)
sensor = 1
datastringOld = ''

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ





while True:
    stamp = time.monotonic()
    humansDetected = 0
    xc = []
    yc = []
    highTemp = 0
    frame = [0] * 768
    try:
        mlx.getFrame(frame)
    except:
        # these happen, no biggie - retry
        continue
    
    
    frame = [int(round(num)) for num in frame]
    frameTemps = frame
    frameTemps = np.reshape(frameTemps, (24, 32))
    for h in range(24):
        for w in range(32):
            if frame[h * 32 + w] > 80:
                highTemp = 1
            if frame[h * 32 + w] < 23 or frame[h * 32 + w] > 31:
                frame[h * 32 + w] = 0
            else:
                frame[h * 32 + w] = 1
    frameEdit = frame 
    frameEdit = np.reshape(frameEdit, (24, 32))
    #print(frameEdit)
    #make cluster
    lw, num = measurements.label(frameEdit)
    
    
    coordinates = lw
    clusters = {} # empty clusters object
    row_num = 0 # row number starts at

    # place a x and y of every number in the array
    for row in coordinates:
        cel_num = 0 # cel_num reset for new row
        for cel in row:
            # 0 doesnt have a value
            # if it exists, +1 otherwise =1
            if cel > 0:
                if str(cel) not in clusters:
                    clusters[str(cel)] = []
                clusters[str(cel)].append({'x': cel_num, 'y': row_num})
            cel_num += 1 # next cel
        row_num += 1 # next row

    # loop through every "clusternumber"
    
    heatmap = []
    
    for cluster_num, cluster_val in clusters.items():
        all_x = [] # every cluster an empty array
        all_y = [] # every cluster an empty array
        for element in cluster_val:
            all_x.append(element['x']) # add all x's to array
            all_y.append(element['y']) # add all y's to array

        x_min = min(all_x) # min x
        x_max = max(all_x) # max x
        y_min = min(all_y) # min y
        y_max = max(all_y) # max y
        


        x_gem = 32 - ((x_min + x_max) / 2) # average X
        y_gem = (y_min + y_max) / 2 # average y

        # every pixel is 1
        area = len(all_x)

        if(area > 45):
            xc = np.append(xc, x_gem)
            yc = np.append(yc, y_gem)
            humansDetected += 1
            #print(frameTemps)
            temperatures = []
            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    # print("%0.0f, " % frameTemps[y][x], end="")
                    temperatures.append(int(frameTemps[y][x]))
                #print()
            #print()
            
            heatmap.append({
                "settings": {
                    "xSize": x_max - x_min + 1,
                    "ySize": y_max - y_min + 1
                    },
                "temps": temperatures
            })
            
        
    clusters = []

    for i in range(0, len(xc)):
        clusters.append({
            "coordinates":{ 
                "x": xc[i],
                "y": yc[i]
                },
            "heatmaps": heatmap
        })
    

    data = {
        "data": {
            "sensor": sensor,
            "humans": humansDetected,
            "tempAlert": highTemp,
            "clusters": clusters,
        }
    }
    
    
    
    datastring = json.dumps(data)
    
    if(datastringOld != datastring):
        publish.single("17089689", datastring, hostname="192.168.0.107")
        print("Sensor read and sent in %0.2f s" % (time.monotonic() - stamp))
        # print(datastring)
    datastringOld = datastring
    # print("end")