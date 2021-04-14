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

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ

frame = [0] * 768
while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue    
    for h in range(24):
        for w in range(32):
            if frame[h * 32 + w] < 24 or frame[h * 32 + w] > 31:
                frame[h * 32 + w] = 0
            #print("%0.0f, " % t, end="")
        #print()
    #print()
    frameEdit = frame
    frameEdit = [int(round(num)) for num in frameEdit]
    frameEdit = np.reshape(frame, (24, 32))
    
    lw, num = measurements.label(frameEdit)
    
    area = measurements.sum(lw, lw, index=arange(lw.max() + 1))
    
    #print(area)
    
    humansDetected = 0
    human = 1
    for i in area:
        if i > 45.0 and i < 80.0:
            location = ndimage.measurements.center_of_mass(lw)
            data = {
                "sensor": sensor,
                #"human": human,
                "x": location[0],
                "y": location[1],
                }
            datastring = json.dumps(data)
            publish.single("17089689", datastring, hostname="192.168.0.107")
            humansDetected += 1
            human += 1
            print("Human detected and sent in %0.2f s" % (time.monotonic() - stamp))
            print(data)
    
    #publish.single("17089689", "blabbla", hostname="192.168.0.107")
    #if humansDetected == 0:
        #print("No human detected")
        
    time.sleep(1)
    



