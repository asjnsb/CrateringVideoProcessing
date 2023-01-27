import cv2
import os

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

#https://www.tutorialspoint.com/how-to-compare-two-images-in-opencv-python