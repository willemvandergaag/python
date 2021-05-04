# import math
# import numpy as np

# a = np.array([[2,3,5], [4,6,7], [1,5,7]])

# print(np.kron(a, np.ones((4,5))))

from datetime import date
import csv

date = str(date.today())

listA = []

i_x = int(1)
i_y = int(2)

print(type(listA))

listA.append(i_x)
listA.append(i_y)


with open('coordinates-' + date + '1.csv', 'a') as myFile:
   writer = csv.writer(myFile)
   writer.writerow(listA)