import os
import cv2
import numpy as np 
import matplotlib.pyplot as plt

def FrameXtract():
    path = dirFinder()
    dir = sorted(os.listdir(path))
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

    print(file+"\n")
    fSkip = int (input("How many frames to skip at a time? "))

    #check for a folder for the frames
    framePath = os.path.join(path,"xtractedFrames", ("%s_Frames_fSkip%d" % (file, fSkip)))
    if os.path.exists(framePath):
        print('Folder already exists: %s' % (framePath))
    else:
        print('New folder: %s' % (framePath))
        os.makedirs(framePath)
        
    if os.listdir(framePath):
        for i in sorted(os.listdir(framePath)):
            if not("frame00000" in i):
                print("Folder is already reduced")
                return(framePath, 0)
            else:
                print("Folder is populated")
                return(framePath, 1)
    else:
        print("Folder is empty")


    print('generating frames...')
    frameN = 0
    while(True):
        if vid.grab():
            if not(frameN%1000):
                print("frameN has surpassed %d" % (frameN))

            if not(frameN%fSkip):
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
    
    print('%d frames generated' % (len(sorted(os.listdir(framePath)))))
    vid.release()
    print('done')
    return(framePath, 1)
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

    #print("Average: %f" %(np.ma.average(yData)))
    #print("MAX: %f" %(np.max(yData)))
    print("Index of MAX: %i" %(yData.index(np.max(yData))))

    plt.plot(yData)
    plt.show()

    start = int(input("Start: "))
    stop = int(input("Stop: "))

    frameDir = sorted(os.listdir(frameFolder))
    if (start < len(yData) and stop < len(yData)):
        cv2.imshow("This should be pre-blasting",cv2.imread(frameFolder+frameDir[start]))
        cv2.imshow("This should be post-blasting",cv2.imread(frameFolder+frameDir[stop]))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Out of range, try again")
    while input("Press ENTER to continue\nOr type any character first to try again\n"):
        start = int(input("Start: "))
        stop = int(input("Stop: "))
        if (start < len(yData) and stop < len(yData)):
            cv2.imshow("This should be pre-blasting",cv2.imread(frameFolder+frameDir[start]))
            cv2.imshow("This should be post-blasting",cv2.imread(frameFolder+frameDir[stop]))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Out of range, try again")
    
    
    print("Deleting frames...")
    i = 0
    for frame in sorted(os.listdir(frameFolder)):
        if int(start) > i or i > int(stop):
            os.remove(frameFolder+frame)
        i += 1
    print("Done")

frameFolder, compNeeded = FrameXtract() #run FrameXtract and save the directory where the frames are stored
frameFolder += '//'
if compNeeded: #this extra assignment step seems to be necessary to split up the tuple that frameComp returns
    frameComp(sorted(os.listdir(frameFolder)))


#LAST: made adjustments for mac