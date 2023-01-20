import cv2
import os

dir = os.listdir()

for i in dir:
    if ".mp4" in i:
        vid = cv2.VideoCapture(i)
        file = i
        break

i = 0
while(True):  
    if not os.path.exists(file):
        print('Folder name: 20221223_121307_Frames{}'.format(i))
        os.makedirs('20221223_121307_Frames{}'.format(i))
        break
    else:
        print('Tried: 20221223_121307_Frames{}'.format(i))
        i+=1

frameN = 0

while(True):
    ret,frame = vid.read()
    
    if ret:
        name = './20221223_121307_Frames/20221223_121307_frame{}.jpg'.format(str(frameN))
        print('generating frame #{}'.format(frameN))

        cv2.imwrite(name, frame)

        frameN+=1
    else:
        break

print('done')
vid.release()
cv2.destroyAllWindows