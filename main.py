import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt

def FrameXtract():
    path = dirFinder()
    dir = os.listdir(path)
    print("Directory contents:", dir)
    search = [".mp4"]
    search.append(input("Search term: "))
    for i in range(len(search)):
        search[i] = search[i].lower()
    
    #find a .mp4 in the current directory
    if dir:
        for i in dir:
            if dir and all([x in i.lower() for x in search]):
                vid = cv2.VideoCapture(os.path.join(path, i))
                file = i[:-4:]
                break
            elif i == dir[len(dir)-1]:
                file = "NotFound"
                raise SystemExit("File not found.")
    else:
        raise SystemExit("Dir is empty")


    #create a folder for the frames
    i = 0
    while(True):
        framePath = os.path.join(path, ("%s_Frames_%d" % (file, i)))
        if not os.path.exists(framePath):
            print('Folder name: %s' % (framePath))
            os.makedirs(framePath)
            newDir = framePath
            break
        else:
            print('Tried: %s' % (framePath))
            i+=1


    print('generating frames...')
    frameN = 0
    while(True):
        ret = vid.grab()
        frame = vid.retrieve()
        #ret is simply whether or not .read() succesfully returned an image
        if ret:
            if frameN < 10:
                name = os.path.join(framePath, '%s_frame00%d.png' % (file, frameN))
            elif frameN < 100:
                name = os.path.join(framePath, '%s_frame0%d.png' % (file, frameN))
            else:
                name = os.path.join(framePath, '%s_frame%d.png' % (file, frameN))
            #print('generating frame #%d' % frameN)

            cv2.imwrite(name, frame)

            frameN+=1
        else:
            break
    print('%d frames generated' % (frameN-1))
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

def dirFinder(): #function to locate/create a folder in the user's videos folder. CURRENTLY ONLY WORKS ON WINDOWS
    absPath = os.path.dirname(__file__)
    head, tail = os.path.split(absPath)
    while "Users" not in os.path.basename(head):
        head, tail = os.path.split(head)

    vidPath = os.path.join(head, tail, "Videos", "CrateringVideos")

    if not os.path.exists(vidPath):
        os.makedirs(vidPath)
        print("Created:", vidPath)
    #else:
    #   print("Path already exists:", vidPath)
    return(vidPath)


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
    
    #cv2.imshow("%s vs %s = %f" %(lasttitle, i, err), diff) #displays all the difference images
    #print("%s vs %s = %f" %(lasttitle, i, err)) #prints all errors
    
    lasttitle = i
    lastImg = curImg
    frameN += 1
#end MSE comparisons

plt.plot(yData)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows

#oldLAST: Found the errors in a real video, but even after plotting, there is no obvious difference in "err" between before and after the jet starts 
#oldNEXT: Try using larger time steps, and don't compare every subsaquent frame.
#LAST: the program now makes and uses a folder in the user's videos folder.
#NEXT: figure out why the frame extractor only gets to 224 frames before cv2 throws a warning and stops. 
#First thing to try: increase OPENCV_FFMPEG_READ_ATTEMPTS. can't figure out how to do this
#Second thing to try: larger time steps. in a 94 second video 224 frames can yield a 0.4s resolution