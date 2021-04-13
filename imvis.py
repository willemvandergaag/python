import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

stamp = time.monotonic()
img = cv2.imread("C:\\Users\\wille\\Desktop\\python\\Original_B.jpg")

blur = cv2.medianBlur(img,5)        # Apply Gaussian Blur to limit noise

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


cv2.imshow("Input", img)
cv2.imshow("output", blur)

cv2.waitKey(0)