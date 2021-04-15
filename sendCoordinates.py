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
sensor = 2
datastringOld = ''

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ

frame = [0] * 768



while True:
    stamp = time.monotonic()
    humansDetected = 0
    xc = []
    yc = []
    highTemp = 0
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue    
    for h in range(24):
        for w in range(32):
            if frame[h * 32 + w] > 80:
                highTemp = 1
            if frame[h * 32 + w] < 24 or frame[h * 32 + w] > 31:
                frame[h * 32 + w] = 0
            else:
                frame[h * 32 + w] = 1
    frameEdit = frame
    frameEdit = [int(round(num)) for num in frameEdit]
    frameEdit = np.reshape(frameEdit, (24, 32))
    #make cluster
    lw, num = measurements.label(frameEdit)   
    
    coordinates = lw
    clusters = {} # empty clusters object
    row_num = 0 # row number starts at

    # zet van van elk getal een {x,y} in de bijbehorende array
    for row in coordinates:
        cel_num = 0 # cel_num weer resetten bij een nieuwe row
        for cel in row:
            # 0 telt niet mee, dus negeren
            # Als hij al bestaat, dan +1 anders =1
            if cel > 0:
                if str(cel) not in clusters:
                    clusters[str(cel)] = []
                clusters[str(cel)].append({'x': cel_num, 'y': row_num})
            cel_num += 1 # we gaan naar de volgende cel
        row_num += 1 # we gaan naar de volgende row

    # loop door elk "clusternummer" heen
    for cluster_num, cluster_val in clusters.items():
        all_x = [] # per cluster een lege array
        all_y = [] # per cluster een lege arrayS
        for element in cluster_val:
            all_x.append(element['x']) # voeg alle x'en toe aan een eigen array
            all_y.append(element['y']) # voeg alle y'en toe aan een eigen array

        x_min = min(all_x) # minimale x
        x_max = max(all_x) # maximale x
        y_min = min(all_y) # minimale y
        y_max = max(all_y) # maximale y

        x_gem = (x_min + x_max) / 2 # bereken de gemiddelde x
        y_gem = (y_min + y_max) / 2 # bereken de gemiddelde y

        area = len(all_x)
        
        if(area > 45 and area < 80):
            xc = np.append(xc, x_gem)
            yc = np.append(yc, y_gem)
            humansDetected += 1
    
    
    clusters = []

    for i in range(0, len(xc)):
        clusters.append({
            "x": xc[i],
            "y": yc[i]
        })
    data = {
        "data": {
            "sensor": sensor,
            "humans": humansDetected,
            "tempAlert": highTemp,
            "clusters": clusters
        }
    }
    datastring = json.dumps(data)
    if(datastringOld != datastring):
        publish.single("17089689", datastring, hostname="192.168.0.107")
        print("Sensor read and sent in %0.2f s" % (time.monotonic() - stamp))
    datastringOld = datastring
    
    
       
    time.sleep(1)
    


