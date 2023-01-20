import cv2
import numpy as np
import matplotlib.pyplot as plt

iSTART = 80
iEND = 100
jEND = 180

image = cv2.imread("20221230_195839.jpg")

#convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#iterate through every combo of thresholds
for i in range(iSTART, iEND+10, 10):
    for j in range(i+10, jEND+10, 10):
        edges = cv2.Canny(gray, threshold1=i, threshold2=j)
        plt.figure()
        plt.imshow(edges, cmap="gray",)
        plt.title("1: {} | 2: {}".format(i,j))
        plt.axis("off")

plt.show()
