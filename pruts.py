import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import cv2
import matplotlib.pyplot as plt

names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

fig = plt.figure(figsize=(9, 3))
plt.subplot(131)
plt.bar(names, values)
plt.subplot(132)
plt.scatter(names, values)
plt.subplot(133)
plt.plot(names, values)
plt.suptitle('Categorical Plotting')



fig.canvas.draw()

print(fig)

img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

 # img is rgb, convert to opencv's default bgr
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

# display image with opencv or any operation you like
cv2.imshow("plot",img)
cv2.waitKey(1)


cv2.waitKey(0)
