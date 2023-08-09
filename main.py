import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt

#CHANGE ME to pick how frequently to generate a frame. [fRate = 5: every 5th frame]
fRate = 10

def FrameXtract():
    path = dirFinder()
    dir = os.listdir(path)
    print("Directory contents:")
    for i in dir:
        print(i)
    search = [".mp4"]
    search.append(input("\nSearch term: "))
    for i in range(len(search)):
        search[i] = search[i].lower()
    
    #find a .mp4 in the current directory
    if dir:
        for i in dir:
            if dir and all([x in i.lower() for x in search]):
                vid = cv2.VideoCapture(os.path.join(path, i))
                file = i[:-4:]
                plt.title(file)
                break
            elif i == dir[len(dir)-1]:
                file = "NotFound"
                raise SystemExit("File not found.")
    else:
        raise SystemExit("Dir is empty")


    #check for a folder for the frames
    framePath = os.path.join(path, ("%s_Frames_fRate%d" % (file, fRate)))
    if os.path.exists(framePath):
        print('Folder already exists: %s' % (framePath))
    else:
        print('New folder: %s' % (framePath))
        os.makedirs(framePath)
        
    if os.listdir(framePath):
        print("Folder is populated")
        return(framePath)
    else:
        print("Folder is empty")


    print('generating frames...')
    frameN = 0
    while(True):
        if vid.grab():
            if not(frameN%1000):
                print("frameN has surpassed %d" % (frameN))

            if not(frameN%fRate):
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

                ret, frame = vid.retrieve()
                #print('generating frame #%d' % frameN)
                cv2.imwrite(name, frame)
        else:
            break
        frameN += 1
    
    print('%d frames generated' % (len(os.listdir(framePath))))
    vid.release()
    print('done')
    return(framePath)
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

def frameComp(frDir):
    print("now calculating img differences")

    xData = []
    yData = []

    frameN = 0
    for i in frDir:
        #find the mean square of the errors between the last image and the current one
        if "frame00000." in i:
            #lasttitle = i
            lastImg = cv2.imread(frameFolder + i)
            continue
        curImg = cv2.imread(frameFolder + i)
        
        err, diff = mse(cv2.cvtColor(lastImg, cv2.COLOR_BGR2GRAY), cv2.cvtColor(curImg, cv2.COLOR_BGR2GRAY))
        
        yData.append(err)
        xData.append(frameN)
        
        #cv2.imshow("%s vs %s = %f" %(lasttitle, i, err), diff) #displays all the difference images
        #print("%s vs %s = %f" %(lasttitle, i, err)) #prints all errors
        #lasttitle = i
        
        lastImg = curImg
        frameN += 1
    return(xData, yData, frameN)
#end MSE comparisons

def mathTime(xData, yData, dir):
    #print("Average: %f" %(np.ma.average(yData)))
    #print("MAX: %f" %(np.max(yData)))
    print("Index of MAX: %i" %(yData.index(np.max(yData))))

    std = np.std(yData)

    plt.plot(yData)

    plt.plot([0,totFrames],[np.ma.average(yData),np.ma.average(yData)])
    plt.plot([0,totFrames],[np.ma.average(yData)+2*std, np.ma.average(yData)+2*std])
    plt.show()
    

    start = input("Start: ")
    stop = input("Stop: ")
    cv2.imshow("This should be pre-blasting",cv2.imread(dir+os.listdir(dir)[int(start)]))
    cv2.imshow("This should be post-blasting",cv2.imread(dir+os.listdir(dir)[int(stop)]))
    if input("Empty = correct\nNotEmpty = wrong"):
        start = input("Start: ")
        stop = input("Stop: ")
        cv2.imshow("This should be pre-blasting",cv2.imread(dir+os.listdir(dir)[int(start)]))
        cv2.imshow("This should be post-blasting",cv2.imread(dir+os.listdir(dir)[int(stop)]))
    cv2.waitKey(0)
    cv2.destroyAllWindows
    


frameFolder = FrameXtract() + '\\' #run FrameXtract and save the directory where the frames are stored
xData, yData, totFrames = frameComp(os.listdir(frameFolder)) #this extra assignment step seems to be necessary to split up the tuple that frameComp returns
mathTime(xData, yData, frameFolder)

#LAST: Switching to having a user say where the start and stop is.
#NEXT: Check that the retry fuction of mathTime() (also rename mathTime()) is working