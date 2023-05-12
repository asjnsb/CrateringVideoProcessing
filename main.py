import cv2
import os
import numpy as np 

def FrameXtract():
    dir = os.listdir()

    #find a .mp4 in the current directory
    for i in dir: 
        if ".mp4" in i:
            vid = cv2.VideoCapture(i)
            file = i[:-4:]
            break

    #create a folder for the frames
    i = 0
    while(True):  
        if not os.path.exists("%s_Frames_%d" % (file, i)):
            print('Folder name: %s_Frames_%d' % (file, i))
            os.makedirs('%s_Frames_%d' % (file, i))
            newDir = '%s_Frames_%d' % (file, i)
            break
        else:
            print('Tried: %s_Frames_%d' % (file, i))
            i+=1


    print('generating frames...')
    frameN = 0
    while(True):
        ret,frame = vid.read()
        
        if ret:
            if frameN < 10:
                name = './%s_Frames_%d/%s_frame0%d.png' % (file, i, file, frameN)
            else:
                name = './%s_Frames_%d/%s_frame%d.png' % (file, i, file, frameN)
            #print('generating frame #%d' % frameN)

            cv2.imwrite(name, frame)

            frameN+=1
        else:
            break
    print('%d frames generated' % frameN)
    vid.release()
    print('done')
    return(newDir)
#end of FrameXtract

def mse(img1, img2): #claculates the mean square of the errors of two images
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff #mse is the value of the error, diff is the visual difference between the images

frameFolder = FrameXtract() + '\\' #run FrameXtract and save the directory where the frames are stored
frDir = os.listdir(frameFolder)

frameN = 0
for i in frDir:
    #find the mean square of the errors between the last image and the current one
    
    if "frame00." in i:
        lasttitle = i
        lastImg = cv2.imread(frameFolder + i)
        continue
    curImg = cv2.imread(frameFolder + i)
    
    err, diff = mse(cv2.cvtColor(lastImg, cv2.COLOR_BGR2GRAY), cv2.cvtColor(curImg, cv2.COLOR_BGR2GRAY))
    
    
    #cv2.imshow("%s vs %s = %f" %(lasttitle, i, err), diff) #displays all the difference images
    #print("%s vs %s = %f" %(lasttitle, i, err)) #prints all errors
    
    lasttitle = i
    lastImg = curImg
    frameN += 1
#end MSE comparisons

cv2.waitKey(0)
cv2.destroyAllWindows

#LAST: program can take a video file, split it into frames, and find the difference between each sequential frame
#NEXT: NEED A REAL VIDEO TO PROGRESS; use the errors to cut out the dead time from the video