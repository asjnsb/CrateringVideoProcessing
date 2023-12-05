# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:39:04 2023

@author: Sudan Devkota
@editor: Aidan St. John Sep 19 2023 ++
"""

import os
import cv2
import statistics
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf) # python truncates the array when printing or writing to file otherwise

#=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=
# Parameters for cropping the image
centerXOff = 75
centerYOff = -75
vCrop = 0.3
hCrop = 0.3
# Parameters for the Canny edge detection (30 & 70 originally)
threshold1 = 20
threshold2 = 60
# Parameters for limiting the number of iterations through the frame files
# None, or 0 for no limit
testLim = 0
frameLim = 0
# Start from a particular test
testStart = 30
#=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=

def imgProcessor(imgPath):
    # Setup variables to be able to save the data to separate files inside the same folder
    # xxFolder = path to the containing folder
    # xxName = just the name of the file
    # xxPath = path to a file, basically xxFolder/xxName
    imgFolder, imgName = os.path.split(imgPath)
    dataFolder = os.path.join(imgFolder, "ContourCoordinates")

    #print(imgName) # to keep track of the progress of the program
    if not os.path.exists(dataFolder):
        print('New folder: %s' % (dataFolder)) # if there isn't a folder already, make one and announce what it is
        os.makedirs(dataFolder)
    dataPath = os.path.join(dataFolder, imgName + "_curveData.txt")
    # Load the image
    image = cv2.imread(imgPath)

    #Find the size of the image:
    width = image.shape[1]
    height = image.shape[0]

    # Define ROI coordinates (top-left and bottom-right)
    roi_tl = (int(width*hCrop)+centerXOff, int(height*vCrop)+centerYOff)  # Example top-left corner (x, y)
    roi_br = (int(width*(1-hCrop))+centerXOff, int(height*(1-vCrop))+centerYOff)  # Example bottom-right corner (x, y)

    # Crop the image to the ROI
    roi_image = image[roi_tl[1]:roi_br[1], roi_tl[0]:roi_br[0]]
    roi_width = roi_image.shape[1]
    roi_height = roi_image.shape[0]
    roi_centerX = int(roi_width/2)
    roi_centerY = int(roi_height/2)

    gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY) # Convert the ROI image to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Apply Gaussian blur to reduce noise and enhance features
    edges = cv2.Canny(blurred, threshold1, threshold2) # Apply Canny edge detection to find edges

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Find contours in the edge-detected image, and return all points (CHAIN_APPROX_NONE)
    contourFile = open(dataPath, "w") # create a file for outputing data

    i = 0
    contourIndex = -1 # if this never gets replaced, then cv2.drawContours will draw all the contours
    for contour in contours:
        for point in contour:# point is a one-element list containing a touple, so point[0] points directly to the tuple. point[1] DNE
            if point[0][0] == (roi_centerX) and point[0][1] > (roi_centerY): 
                contourIndex = i
        i += 1
    # if there's no contour below the center, check above the center
    i = 0
    prevPoint = 0
    if contourIndex == -1:
        for contour in contours:
            for point in contour:
                # the below if logic should result in selecting the closest contour that is directly above the center point
                if (point[0][0] == (roi_centerX) and point[0][1] < (roi_centerY)) and point[0][1] > prevPoint:
                    prevPoint = point[0][1]
                    contourIndex = i
            i += 1


    if contourIndex == -1:
        # don't write the data to a file if all the contours are being drawn
        contourFile.write("Couldn't isolate a contour")
    else:
        # write the data to a text file where each line after the first is an x-y coordinate separated by a space and no brackets
        contourFile.write(" X   Y\n")
        for i in contours[contourIndex]:
            contourFile.write("%s %s\n"%(i[0][0], i[0][1]))
    contourFile.close()

    drawnContours = cv2.drawContours(roi_image, contours, contourIndex, (0, 255, 0), 1) # Draw the contours (img, contours, which contour?, color, line width)

    #draw a small circle in the center of the image
    drawnContours = cv2.circle(drawnContours, [roi_centerX, roi_centerY], 1, [0,0,255],-1)

    # Display the image with contours overlayed
    #cv2.imshow(imgName, drawnContours)
    """# Display the image with detected parabolic curves in the ROI
    cv2.imshow("Detected Parabolic Curves in ROI", roi_image)"""
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    return(dataFolder)

def dirFinder(): #function to locate/create a folder in the user's videos folder. CURRENTLY ONLY WORKS ON WINDOWS
    absPath = os.path.dirname(__file__)
    head, tail = os.path.split(absPath)
    while "Users" not in os.path.basename(head):
        head, tail = os.path.split(head)

    vidPath = os.path.join(head, tail, "Videos", "CrateringVideos", "xtractedFrames")
    
    if not os.path.exists(vidPath):
        os.makedirs(vidPath)
        print("Created:", vidPath)
        print("Go put stuff in this folder")
    #else:
    #   print("Path already exists:", vidPath)
    return(vidPath)

def plotter(x, y, fileName):
    # plot (scatter) the values created in coodAdjuster. 
    # np.asarray(xx, float) ensures that the axies aren't unreadable from too many ticks
    # s=x sets the size of the points
    plt.scatter(np.asarray(x, float), np.asarray(y, float), s=1)
    plt.title(fileName)
    plt.axis('equal')
    plt.show()

class coodAdjusterClass:
    def __init__ (self):
        self.data = []
        self.x = []
        self.y = []
        self.lower = 0
        self.upper = 1000000

    def coodAdjuster(self, dataFolder):
        # iterate over the .txts that are in dataFolder to adjust the data
        for fileName in os.listdir(dataFolder): 
            dataPath = os.path.join(dataFolder, fileName)
            _ , extension = os.path.splitext(fileName)

            localData = []

            # reads the data in dataPath into the array localData
            if "txt" in extension: # skips anything that isn't a .txt
                dataFile = open(dataPath, "r")
                for i in dataFile.readlines():
                    localData.append(i.split())
            
            dataFile.close()
            
            localData.pop(0) # removes the first item in data, which would be the title line of the dataFile
            self.data.extend(localData) # moves the data just generated into the data variable that will persist across executions
            self.x, self.y = zip(*self.data) # splits the data into a format that plotter() can take
        
        plotter(self.x, self.y, fileName)
        trimmedX = []
        trimmedY = []
        
        while not input("Enter Enter to trim the data, or anything else to continue\n"):
            trimmedX = []
            trimmedY = []    
            
            self.lower = int(input("Lower bound = "))
            self.upper = int(input("Upper bound = "))
            
            index = 0
            for n in self.x:
                o = int(n)
                if o > self.lower and o < self.upper:
                    trimmedX.append(o)
                    trimmedY.append(int(self.y[index]))
                index += 1
            plotter(trimmedX, trimmedY, fileName)

        #if trimmedX is empty, continue
        if  not trimmedX:
            return

        #find the indices and values of the the points that are on the rightmost and leftmost edge of the data (within a bound)
        leftEdgeIndices = []
        rightEdgeIndices = []
        lEValues = []
        rEValues = []
        for i in range(len(trimmedX)):
            if abs(trimmedX[i]-self.lower) < 2:
                leftEdgeIndices.append(i)
                lEValues.append(trimmedY[i])
            if abs(trimmedX[i]-self.upper) < 2:
                rightEdgeIndices.append(i)
                rEValues.append(trimmedY[i])

        #find new location for the origin by averaging the median of both ends of the data
        leftM = statistics.median(lEValues)
        rightM = statistics.median(rEValues)
        self.newYOrigin = (leftM + rightM)/2       
        self.newXOrigin = statistics.mean(trimmedX)

        #Plot the transformed data
        plotter([x-self.newXOrigin for x in trimmedX], [-1*(y-self.newYOrigin) for y in trimmedY], "Transformed data")

        self.fileReWriter(dataFolder)

        #clear out the data between folders
        self.data = []
    
    def fileReWriter(self, dataFolder):
            # this contains the same logic at the beginning of coodAdjuster, but for writing rather than reading
            for fileName in os.listdir(dataFolder):
                dataPath = os.path.join(dataFolder, fileName)
                _ , extension = os.path.splitext(fileName)
                
                localData = []
                if "txt" in extension:
                    dataFile = open(dataPath, "r")
                    for i in dataFile.readlines():
                        localData.append(i.split())
                else:
                    #this is meant to make it so that I don't have to double check for "txt" again, but idk if it does
                    continue
                dataFile.close()

                localData.pop(0)
                if localData:
                    oldX, oldY = zip(*localData)
                newX = []
                newY = []
                
                #trim the data from each file independently
                for i in range(len(oldX)):
                    if int(oldX[i]) < self.upper and int(oldX[i]) > self.lower:
                        newX.append(int(oldX[i]))
                        newY.append(int(oldY[i]))
                
                #adjust the origin and orientation of the data
                newX = [x-self.newXOrigin for x in newX]
                newY = [-1*(y-self.newYOrigin) for y in newY]

                #write trimmedX and trimmedY to each file
                dataFile = open(dataPath, "w")
                dataFile.write(" X  Y")
                for i in range(len(newX)):
                    dataFile.writelines("\n" + str(newX[i]) + " " + str(newY[i]))
                dataFile.close()

                """dataFile = open(dataPath, "r")
                localData = [i.split() for i in dataFile.readlines()]
                localData.pop(0)
                x, y = zip(*localData)
                plotter(x, y, "From the file")"""

                




frameFolder = dirFinder()

videoData = coodAdjusterClass()

# nested loops for iterating over every frame image in every frame folder
k = 0
for i in os.listdir(frameFolder):
    if k < testStart:
        k += 1
        continue
    print("Test Number {}".format(k))
    print("Frames Folder: {}".format(i))
    l = 0
    for j in os.listdir(os.path.join(frameFolder, i)):
        framePath = os.path.join(frameFolder, i, j)
        _ , extension = os.path.splitext(framePath)

        if extension: # this checks that framePath is a file and not just a folder
            dataFolder = imgProcessor(framePath) # imgProcessor returns the contour data path

        # to check that frameLim != None and that it hasn't been exceeded
        if frameLim and l >= frameLim: 
            break
        l += 1

    videoData.coodAdjuster(dataFolder)
    
    # to check that testLim != None and that it hasn't been exceeded
    if testLim and k >= testLim-1: 
        break
    k += 1


#LAST: Worked on tuning the edge finder, I think for many videos, there will simply be no hope. The previous settings were really good, and I ended up quite close.
#NEXT: Pick the best thresholds and go through all the videos
#ALSO: This get stuck in line 111 bc my documents folder is not in my C: drive on my desktop
#PLAN: manual selection of crater center & edges: show the user a bunch of plots from one video, then prompt them for the desired values, then draw those values over the plots and double check with the user.



# Old code for fitting a parabola to the contours
"""# Define the y-coordinate threshold for excluding contours below it
y_threshold = 500  # Adjust this value based on your image

# Loop through the detected contours
for contour in contours:
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Exclude contours below the y-coordinate threshold
    if y < y_threshold:
        # Fit a curve to the contour using polynomial approximation
        if len(contour) > 1:
            # Get x and y values from the contour points
            x = contour[:, 0, 0]
            y = contour[:, 0, 1]
            
            # Fit a 2nd-degree polynomial (parabola)
            z = np.polyfit(x, y, 2)
            fit_curve = np.poly1d(z)
            
            # Generate x values for plotting
            x_fit = np.linspace(min(x), max(x), 100)
            y_fit = fit_curve(x_fit)
            
            # Draw the parabolic curve
            for i in range(len(x_fit) - 1):
                cv2.line(roi_image, (int(x_fit[i]), int(y_fit[i])), (int(x_fit[i + 1]), int(y_fit[i + 1])), (0, 255, 0), 2)

print("%s, %s" %(x, y))"""