import numpy as np
import cv2, math

distanceY = 0

if not distanceY:
    distanceY = int(input("Distance between 2 sensors in cm: "))
    if distanceY >= 70 and distanceY < 80:
        iterationsAlpha = 28
        iterationsBeta = 2
        length = 57
    elif distanceY >= 80 and distanceY < 100:
        iterationsAlpha = 28
        iterationsBeta = 2
        length = 59
    elif distanceY >= 100 and distanceY < 120:
        iterationsAlpha = 29
        iterationsBeta = 1
        length = 61
    elif distanceY >= 120:
        iterationsAlpha = 30
        iterationsBeta = 0
        length = 63
    elif distanceY > 140:
        print("Sensors too far apart!")
        exit()

frame = [0] * distanceY * 24
prevData = []
nmin = 0
nmax = 255
alpha1 = 0.5
alpha2 = 0.5

while True:
    heatmap = np.zeros((distanceY,24,3), np.uint8) #create the blank image to work from
    data = np.genfromtxt(r"C:\\Users\\wille\\Desktop\\python\\data.csv", delimiter = ',') #get the data
    print("Data:")
    print(data)
    print(len(data))
    num_rows, num_cols = data.shape

    if np.array_equal(data,prevData):
	    print('No new data yet')
    
    minValue = math.floor(np.amin(data))
    maxValue = math.ceil(np.amax(data))
    outputEE = data - minValue      
    outputEE = outputEE * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

    # resize image
    #num_cols = num_cols * 10
    dim = (num_cols * 10, num_rows * 10)
    outputEE = cv2.resize(outputEE, dim, interpolation = cv2.INTER_LINEAR )

    # apply colormap
    imgEGray = outputEE.astype(np.uint8)
    imgE = cv2.applyColorMap(imgEGray, cv2.COLORMAP_JET)

	# Display the resulting frame
    cv2.namedWindow('Thermal',cv2.WINDOW_NORMAL)

    cv2.imshow('Thermal',imgE)


    res = cv2.waitKey(1)
	#print(res)

