import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt

#CHANGE ME to pick how frequently to generate a frame. [fRate = 5: every 5th frame]
fRate = 10

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
        if vid.grab():
            if frameN < 10:
                name = os.path.join(framePath, '%s_frame0000%d.png' % (file, frameN))
            elif frameN < 100:
                name = os.path.join(framePath, '%s_frame000%d.png' % (file, frameN))
            elif frameN < 1000:
                name = os.path.join(framePath, '%s_frame00%d.png' % (file, frameN))
            elif frameN < 10000:
                name = os.path.join(framePath, '%s_frame0%d.png' % (file, frameN))
            else:
                name = os.path.join(framePath, '%s_frame%d.png' % (file, frameN))
            
            if not(frameN%1000):
                print("frameN has surpassed %d" % (frameN))

            if not(frameN%fRate):
                ret, frame = vid.retrieve()
                #print('generating frame #%d' % frameN)
                cv2.imwrite(name, frame)
        else:
            break
        frameN += 1
    
    print('%d frames generated' % (len(os.listdir(framePath))))
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

print("now calculating img differences")

xData = []
yData = []

frameN = 10
for i in frDir:
    #find the mean square of the errors between the last image and the current one
    if "frame00000." in i:
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

#LAST: the program can sucessfully get through an entire video. This was accomplished by manually using VLC to convert each video to the same video format it was already in
#NEXT: the graph does seem to be helpful, but mostly only for the beginning. Try using .rolling() to calculate a rolling average difference to find spikes.