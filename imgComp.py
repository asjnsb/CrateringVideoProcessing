import cv2
import numpy as np

def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse


img0 = cv2.cvtColor(cv2.imread('heartless.jpg'), cv2.COLOR_BGR2GRAY)
img1 = cv2.cvtColor(cv2.imread('hearts.jpg'), cv2.COLOR_BGR2GRAY)

cv2.imshow("img0", img0)
cv2.waitKey(0)
cv2.destroyAllWindows