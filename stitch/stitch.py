import cv2
import time

stamp = time.monotonic()
stitcher = cv2.Stitcher.create()
foo = cv2.imread("C:/Users/wille/Desktop/python/102-hot_object.jpg")
bar = cv2.imread("C:/Users/wille/Desktop/python/106-hot_object.jpg")
result = stitcher.stitch((foo,bar))

cv2.imwrite("C:/Users/wille/Desktop/python/object.jpg", result[1])
print("stitching completed in %0.2f s" %(time.monotonic() - stamp))