import numpy as np
import cv2, math

scaling = 10

width = scaling * 32
height = scaling * 24

alpha = "23, 22, 24, 24, 26, 27, 26, 26, 25, 26, 28, 28, 25, 24, 23, 23, 22, 22, 22, 21, 22, 21, 21, 21, 22, 21, 22, 22, 21, 21, 20, 20, 22, 23, 23, 26, 27, 27, 26, 27, 27, 26, 25, 25, 24, 23, 22, 23, 22, 22, 22, 22, 21, 22, 21, 20, 21, 21, 21, 22, 21, 21, 20, 21, 24, 23, 25, 26, 28, 28, 26, 26, 26, 25, 23, 23, 22, 22, 23, 22, 22, 22, 22, 22, 21, 21, 22, 21, 21, 21, 22, 22, 21, 21, 20, 22, 24, 24, 24, 26, 27, 27, 27, 27, 26, 24, 22, 22, 22, 22, 22, 23, 22, 22, 21, 22, 21, 21, 21, 22, 20, 22, 21, 21, 22, 21, 22, 21, 23, 22, 22, 24, 23, 24, 24, 23, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 22, 21, 22, 21, 21, 21, 21, 21, 21, 21, 22, 21, 21, 21, 21, 22, 21, 22, 22, 21, 22, 22, 22, 21, 22, 22, 22, 22, 21, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 20, 21, 21, 21, 22, 21, 21, 21, 21, 22, 22, 21, 21, 21, 21, 22, 22, 21, 21, 22, 22, 21, 22, 22, 21, 21, 21, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 21, 22, 21, 22, 22, 22, 22, 22, 21, 22, 21, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 21, 21, 21, 22, 21, 21, 21, 21, 21, 22, 22, 22, 21, 22, 22, 22, 22, 21, 21, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 21, 21, 22, 21, 21, 21, 22, 21, 22, 22, 22, 22, 21, 22, 22, 22, 21, 21, 22, 21, 22, 22, 22, 21, 21, 21, 22, 21, 21, 21, 22, 21, 21, 21, 22, 21, 21, 21, 21, 22, 22, 23, 24, 27, 26, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 22, 21, 21, 21, 21, 22, 21, 22, 21, 22, 21, 21, 21, 21, 22, 22, 22, 26, 30, 36, 31, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 21, 21, 21, 21, 22, 23, 26, 30, 31, 25, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 24, 25, 23, 23, 22, 23, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 21, 22, 21, 21, 21, 22, 21, 21, 21, 22, 21, 21, 21, 22, 22, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 21, 21, 21, 21, 22, 21, 21, 21, 21, 21, 21, 21, 22, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 22, 22, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 21, 21, 21, 21, 21, 22, 21, 22, 22, 22, 22, 23, 22, 22, 23, 22, 22, 22, 22, 22, 22, 21, 22, 21, 20, 21, 21, 21, 22, 21, 21, 21, 21, 20, 20, 21, 21, 21, 21, 21, 22, 22, 22, 23, 23, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22, 21, 21, 21, 22, 22, 20, 21, 22, 21, 21, 21, 21, 21, 20, 22, 21, 22, 21, 22, 22, 22, 22, 21, 22, 22, 22, 23, 22, 22, 21, 21, 22, 21, 22, 21, 21, 22, 21, 21, 21, 20, 21, 20, 21, 21, 21, 21, 21, 22, 21, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 22, 22, 21, 22, 22, 21, 21, 22, 21, 21, 20, 21, 21, 20, 21, 21, 21, 21, 21, 22, 21, 22, 21, 22, 22, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 21, 22, 21, 20, 21, 21, 20, 20, 21, 21, 20, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 21, 22, 22, 21, 22, 22, 22, 22, 21, 22, 21, 21, 21, 21, 21, 21, 21, 21, 19, 20, 21, 22, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 21, 22, 22, 21, 22, 22, 21, 22, 21, 21, 21, 21, 21, 22, 20, 22, 20, 20, 22, 21, 22, 20, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 21, 22, 21, 22, 22, 22, 21, 22, 21, 22, 22, 21, 21, 21, 21, 21"
beta = "24, 23, 23, 22, 22, 22, 22, 21, 21, 21, 23, 22, 22, 22, 22, 22, 23, 23, 24, 25, 27, 26, 27, 27, 26, 27, 27, 26, 25, 25, 25, 24, 23, 23, 22, 23, 23, 22, 22, 21, 21, 21, 22, 21, 22, 22, 23, 23, 23, 23, 25, 28, 29, 28, 28, 27, 27, 27, 28, 27, 25, 25, 25, 25, 23, 22, 24, 23, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 22, 23, 24, 24, 28, 30, 30, 29, 28, 27, 29, 30, 28, 27, 25, 25, 23, 24, 23, 23, 23, 23, 22, 22, 22, 23, 22, 22, 22, 22, 22, 23, 22, 22, 23, 24, 29, 29, 30, 30, 27, 27, 30, 30, 29, 27, 24, 24, 24, 24, 23, 22, 23, 23, 23, 22, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 28, 28, 29, 30, 29, 28, 27, 28, 27, 26, 24, 24, 24, 24, 23, 22, 23, 23, 22, 23, 23, 22, 22, 21, 22, 23, 22, 22, 22, 22, 23, 23, 26, 28, 29, 28, 29, 29, 27, 25, 25, 26, 23, 23, 24, 24, 23, 24, 23, 22, 23, 22, 23, 22, 22, 22, 22, 22, 22, 23, 22, 22, 23, 22, 23, 24, 25, 25, 26, 25, 23, 23, 24, 23, 23, 24, 23, 23, 23, 22, 23, 23, 23, 22, 22, 23, 22, 22, 22, 23, 22, 22, 22, 23, 22, 22, 23, 23, 23, 23, 24, 23, 22, 23, 24, 24, 24, 24, 23, 23, 23, 23, 23, 23, 23, 22, 23, 22, 22, 22, 22, 23, 22, 22, 22, 22, 22, 23, 22, 22, 22, 23, 23, 22, 23, 23, 23, 23, 22, 23, 24, 23, 23, 23, 23, 23, 23, 23, 22, 23, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 22, 23, 23, 23, 23, 24, 22, 23, 22, 23, 24, 23, 23, 22, 23, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 23, 23, 23, 22, 23, 22, 22, 22, 23, 23, 23, 23, 23, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 22, 22, 22, 22, 23, 22, 22, 22, 22, 23, 23, 23, 23, 22, 23, 22, 23, 23, 23, 23, 23, 22, 22, 22, 23, 23, 23, 22, 23, 23, 23, 23, 23, 22, 22, 23, 23, 22, 22, 22, 22, 22, 22, 22, 23, 23, 24, 24, 23, 23, 23, 23, 23, 22, 22, 22, 23, 23, 23, 22, 23, 23, 22, 22, 22, 22, 23, 23, 22, 22, 22, 22, 22, 22, 23, 22, 24, 26, 30, 28, 24, 24, 23, 23, 23, 23, 23, 22, 23, 23, 23, 23, 23, 21, 22, 23, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 23, 26, 34, 37, 29, 24, 23, 24, 23, 23, 23, 23, 23, 23, 23, 23, 24, 22, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 25, 27, 29, 27, 24, 24, 23, 23, 23, 23, 23, 22, 24, 22, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 22, 22, 22, 22, 22, 22, 22, 23, 23, 24, 24, 24, 24, 23, 23, 24, 23, 23, 22, 22, 22, 23, 22, 22, 22, 22, 23, 22, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 24, 24, 24, 24, 24, 24, 22, 23, 22, 24, 23, 23, 22, 23, 23, 22, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 24, 23, 23, 23, 24, 24, 23, 23, 23, 22, 23, 22, 21, 22, 23, 23, 22, 23, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 22, 23, 23, 23, 23, 22, 22, 23, 22, 23, 23, 23, 22, 23, 22, 22, 22, 22, 22, 22, 22, 23, 22, 22, 23, 23, 23, 23, 23, 24, 23, 23, 23, 23, 23, 22, 23, 22, 23, 22, 22, 23, 23, 23, 23, 23, 23, 23, 22, 22, 22, 22, 22, 22, 23, 22, 23, 23, 23, 23, 23, 23, 23, 23, 22, 22, 20, 23, 22, 22, 22, 22, 23, 22, 22, 22, 23, 23, 22, 22, 23, 22, 22, 22, 22, 22, 23, 22, 23, 23, 23, 23, 23, 22, 22, 23, 23, 24, 21, 22, 22, 22, 22, 23, 23, 23, 23, 22, 23, 23, 23, 22, 22, 22, 22, 22, 22, 23, 22, 22, 23, 23, 22, 23, 23, 23, 23, 23, 23, 24"

B = np.matrix(alpha)
A = np.matrix(beta)

# print("A =", A) 
# print("B =", B)

outputA = A.reshape(24,32)
outputB = B.reshape(24,32)
outputC = A.reshape(24,32)
outputD = B.reshape(24,32)

iterationsAlpha = 23
iterationsListAlpha = list(range(iterationsAlpha, 32))
print(iterationsListAlpha)

iterationsBeta = 8
iterationsListBeta = list(range(0, iterationsBeta + 1))
print(iterationsListBeta)

outputC = np.delete(outputC, iterationsListAlpha, 1)
outputD = np.delete(outputD, iterationsListBeta, 1)

print(outputC)
print(outputD)

###################

outputE = np.append(outputC, outputD, axis=1)
num_rows, num_cols = outputE.shape


minValue = math.floor(np.amin(outputE))
maxValue = math.ceil(np.amax(outputE))
outputE = outputE - minValue      
outputE = outputE * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

# resize image
num_cols = num_cols * 10
dim = (num_cols, height)

print(num_cols)
print(height)
outputE = cv2.resize(outputE, dim, interpolation = cv2.INTER_LINEAR )

# apply colormap
imgEGray = outputE.astype(np.uint8)
imgE = cv2.applyColorMap(imgEGray, cv2.COLORMAP_JET)

cv2.imshow("merged with cutting", imgE)

###########################
outputD = np.append(outputA, outputB, axis=1)

minValue = math.floor(np.amin(outputD))
maxValue = math.ceil(np.amax(outputD))
outputD = outputD - minValue      
outputD = outputD * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

# resize image
dim = (width * 2, height)
outputD = cv2.resize(outputD, dim, interpolation = cv2.INTER_LINEAR )

# apply colormap
imgDGray = outputD.astype(np.uint8)
imgD = cv2.applyColorMap(imgDGray, cv2.COLORMAP_JET)

winname = "merged without cutting"
cv2.namedWindow(winname)        # Create a named window
cv2.moveWindow(winname, 40,30)  # Move it to (40,30)
cv2.imshow(winname, imgD)

#############################

minValue = math.floor(np.amin(outputB))
maxValue = math.ceil(np.amax(outputB))
outputBB = outputB - minValue      
outputBB = outputBB * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

# resize image
dim = (width, height)
outputBB = cv2.resize(outputBB, dim, interpolation = cv2.INTER_LINEAR )

# apply colormap
imgBGray = outputBB.astype(np.uint8)
imgB = cv2.applyColorMap(imgBGray, cv2.COLORMAP_JET)

# ####################

minValue = math.floor(np.amin(outputA))
maxValue = math.ceil(np.amax(outputA))
outputAA = outputA - minValue      
outputAA = outputAA * 255/ (maxValue - minValue) # Now scaled to 0 - 255   

# resize image
dim = (width, height)
outputAA = cv2.resize(outputAA, dim, interpolation = cv2.INTER_LINEAR )

# apply colormap
imgAGray = outputAA.astype(np.uint8)
imgA = cv2.applyColorMap(imgAGray, cv2.COLORMAP_JET)

#########################

cv2.imshow("Original B", imgB)
cv2.imshow("Original A", imgA)


#cv2.imshow("Merged without cutting", imgD)

cv2.waitKey(0)