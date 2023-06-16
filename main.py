import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt

def FrameXtract():
    dir = os.listdir()
    search = [".mp4"]
    search.append(input("Search term: "))
    for i in range(len(search)):
        search[i] = search[i].lower()

    #find a .mp4 in the current directory
    for i in dir:
        if all([x in i.lower() for x in search]):
            vid = cv2.VideoCapture(i)
            file = i[:-4:]
            break
        elif i == dir[len(dir)-1]:
            file = "NotFound"
            raise SystemExit("File not found.")


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
                name = './%s_Frames_%d/%s_frame00%d.png' % (file, i, file, frameN)
            elif frameN < 100:
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

xData = []
yData = []

frameN = 0
for i in frDir:
    #find the mean square of the errors between the last image and the current one
    
    if "frame000." in i:
        lasttitle = i
        lastImg = cv2.imread(frameFolder + i)
        continue
    curImg = cv2.imread(frameFolder + i)
    
    err, diff = mse(cv2.cvtColor(lastImg, cv2.COLOR_BGR2GRAY), cv2.cvtColor(curImg, cv2.COLOR_BGR2GRAY))
    
    yData.append(err)
    xData.append(frameN)
    
    cv2.imshow("%s vs %s = %f" %(lasttitle, i, err), diff) #displays all the difference images
    #print("%s vs %s = %f" %(lasttitle, i, err)) #prints all errors
    
    lasttitle = i
    lastImg = curImg
    frameN += 1
#end MSE comparisons

plt.plot(yData)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows

#LAST: Found the errors in a real video, but even after plotting, there is no obvious difference in "err" between before and after the jet starts 
#NEXT: Try using larger time steps, and don't compare every subsaquent frame