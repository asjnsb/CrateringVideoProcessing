import cv2
import numpy as np

def mse(img0, img1):
    h, w = img0.shape
    diff = cv2.subtract(img0, img1)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse


img0 = cv2.cvtColor(cv2.imread('heartless.jpg'), cv2.COLOR_BGR2GRAY)
img1 = cv2.cvtColor(cv2.imread('hearts.jpg'), cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(cv2.imread('Beach.jpg'), cv2.COLOR_BGR2GRAY)


error = mse(img0, img1)
error1 = mse(img0, img2)

print("Image matching Error between img0 & img1:", error)
print("Image matching Error between img0 & img2:", error1)
#cv2.imshow("img0", img0)
#cv2.imshow("img1", img1)
#cv2.imshow("img2", img2)
cv2.waitKey(0)
cv2.destroyAllWindows