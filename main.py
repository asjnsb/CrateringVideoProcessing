import cv2
import os
import numpy as np 

def FrameXtract():
    dir = os.listdir()

    for i in dir:
        if ".mp4" in i:
            vid = cv2.VideoCapture(i)
            file = i[:-4:]
            break



    i = 0
    while(True):  
        if not os.path.exists("%s_Frames_%d" % (file, i)):
            print('Folder name: %s_Frames_%d' % (file, i))
            os.makedirs('%s_Frames_%d' % (file, i))
            break
        else:
            print('Tried: 20221223_121307_Frames_%d' % i)
            i+=1

    frameN = 0
    while(True):
        ret,frame = vid.read()
        
        if ret:
            name = './%s_Frames_%d/%s_frame%d.png' % (file, i, file, frameN)
            print('generating frame #%d' % frameN)

            cv2.imwrite(name, frame)

            frameN+=1
        else:
            break

    print('done')
    vid.release()
#end of FrameXtract


def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
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