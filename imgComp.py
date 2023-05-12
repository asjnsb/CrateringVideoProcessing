import cv2
import numpy as np

def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff

img0 = cv2.cvtColor(cv2.imread('shortziggy_frame65.png'), cv2.COLOR_BGR2GRAY)
img1 = cv2.cvtColor(cv2.imread('shortziggy_frame66.png'), cv2.COLOR_BGR2GRAY)
#img2 = cv2.cvtColor(cv2.imread('Beach.jpg'), cv2.COLOR_BGR2GRAY)


error, diff0 = mse(img0, img1)
#error1, diff1 = mse(img0, img2)

print("Image matching Error between img0 & img1:", error)
#print("Image matching Error between img0 & img2:", error1)
#cv2.imshow("img0", img0)
#cv2.imshow("img1", img1)
#cv2.imshow("img2", img2)
cv2.imshow("difference between 0 & 1", diff0)
#cv2.imshow("difference between 0 & 2", diff1)
cv2.waitKey(0)
cv2.destroyAllWindows