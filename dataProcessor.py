#!/usr/bin/python

import os
import math
import numpy as np
import matplotlib.pyplot as plt

#=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=
# Parameters for limiting the number of iterations through the frame files
# None, or 0 for no limit
testLim = 1
frameLim = 0
# Start from a particular test
testStart = 0
#=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=

def dirFinder(): #function to locate a folder in the user's videos folder. CURRENTLY ONLY WORKS ON WINDOWS
    absPath = os.path.dirname(__file__)
    head, tail = os.path.split(absPath)
    while "Users" not in os.path.basename(head):
        head, tail = os.path.split(head)

    path = os.path.join(head, tail, "Videos", "CrateringVideos", "xtractedFrames")

    if not os.path.exists(path):
        return("Path Not Found")

    return(path)

# data must be in the form of a list of tuples
def volFunc(data):
    x = []
    y = []
    volume = 0.0

    for i in data:
        x.append(float(i[0])/40) # separate out the x and y values and convert from pixels to cm
        y.append(float(i[1])/40)
    
    xm = sum(x)/len(x)
    r = [i-xm for i in x]
    for j in range(len(x)):
        #skip j = 0 so that j-1 is not out of bounds
        if j == 0:
            continue
        deltaY = abs(y[j]-y[j-1])

        volume += 0.5*deltaY*(math.pi*((r[j]+r[j-1  ])/2.0)**2.0)

    return(volume)

def depthFunc(data):
    x = []
    y = []

    for i in data:
        x.append(float(i[0])/40) # separate out the x and y values and convert from pixels to cm
        y.append(float(i[1])/40)
    
    max = y[0]
    min = y[0]
    for i in y:
        if i > max:
            max = i
        if i < min:
            min = i
    #Print statement for debugging. Feels like depth is not being calculated correctly
    #print("min = {}, max = {}, diff = {}".format(min, max, max-min))
    #very simple way of doing this, but we'll start here.
    return max - min

Path = dirFinder()
if "Path Not Found" in Path:
    print("{}, exiting...".format(Path))
    raise SystemExit(0)

# nested loops for looping through all tests and all frames from each test
k = 0
for fileName in os.listdir(Path): #iterates over all items in path
    #skips everything that has an extension (all non-folders)
    _, ext = os.path.splitext(fileName)
    if ext:
        continue

    #skips all files up to the test number specified by testStart
    if k < testStart:
        k += 1
        continue
    
    #print the current test being worked on
    print("Test Number {}".format(k))
    print("Frames Folder: {}".format(fileName))

    #prep for the coming loop
    contourPath = os.path.join(Path, fileName, "ContourCoordinates")
    volumeFile = open(os.path.join(Path, "{}_VOLUMES.txt".format(fileName)), "w") #ensures volumeFile is empty
    volumeFile = open(os.path.join(Path, "{}_VOLUMES.txt".format(fileName)), "a") #allows me to append to volumeFile
    volumeFile.write("Contour Number, volume of contour (cm^3)\n")

    depthFile = open(os.path.join(Path, "{}_DEPTHS.txt".format(fileName)), "w") #ensures depthFile is empty
    depthFile = open(os.path.join(Path, "{}_DEPTHS.txt".format(fileName)), "a") #allows me to append to depthFile
    depthFile.write("Contour Number, Depth of contour (cm)\n")

    dataCollector = []
    l = 0
    for contour in os.listdir(contourPath):
        #ensures that the program is only opening text files
        _, ext = os.path.splitext(contour)
        if ".txt" in ext:
            data = [] 
            dataFile = open(os.path.join(contourPath, contour), "r")
            #read all the lines of the data file into a variable as tuples
            for i in dataFile.readlines():
                data.append(i.split())
            #delete the first line of data because it doesn't contain any data
            if "Couldn't" in data[0]:
                continue
            data.pop(0)

            #print(contour)
            vol = volFunc(data)
            volumeFile.write("{}, {:.4f}\n".format(l, vol))
            depth = depthFunc(data)
            depthFile.write("{}, {:.4f}\n".format(l, depth))
            
            if frameLim and l >= frameLim-1:
                break
            l += 1
    dataFile.close()
    volumeFile.close()
    depthFile.close()
    # to check that testLim != None and that it hasn't been exceeded
    if testLim and k >= testLim-1:
        break
    k += 1

#REPORT: Trying to calculate depth. Implemented one method that should work but I'm suspicous of it.

"""old code below""""""
data = np.loadtxt("SetA1HOOSH.csv", delimiter=',', skiprows=1, unpack=True)

x = data[2,0:501]
y = data[3,0:501]
xm = sum(x)/502
print("mean position of the crater")
print(xm)
r= abs(x - xm)
#print(r)
volume=0.0

#for first crator
for i in range(np.size(data[0,0:16])-1):
    deltaY = abs(y[i+1]-y[i])
    "Using mean radius"
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)
print("Total volume of the craters Inch^3")    
print("%1.3e" % volume)

#for second crator
for i in range(np.size(data[0,17:43])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for third crator
for i in range(np.size(data[0,44:72])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for forth crator
for i in range(np.size(data[0,73:103])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for fifth crator
for i in range(np.size(data[0,104:136])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for eighth crator
for i in range(np.size(data[0,137:169])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for nineth crator
for i in range(np.size(data[0,170:203])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)


#for 10th crator
for i in range(np.size(data[0,204:238])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 11th crator
for i in range(np.size(data[0,239:274])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 12th crator
for i in range(np.size(data[0,275:310])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 13th crator
for i in range(np.size(data[0,311:347])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 14th crator
for i in range(np.size(data[0,348:385])-1):
    deltaY = y[i+1]-y[i]
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 15th crator
for i in range(np.size(data[0,386:424])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 16th crator
for i in range(np.size(data[0,425:462])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

#for 17th crator
for i in range(np.size(data[0,463:501])-1):
    deltaY = abs(y[i+1]-y[i])
    volume += 0.5*deltaY*(math.pi*((r[i+1]+r[i])/2.0)**2.0)  
print("%1.3e" % volume)

np.savetxt('SetA1HOOSH.txt',r, fmt='%1.4e')
#np.savetxt('Sand2bW_volume.txt',volume, fmt='%1.4e')

#outfile=open("Sand2BW_radius.txt", 'a')
#outfile.write(r)
#outfile.close()
#plt.plot(x,y,'ro', mew = 0.5)
#plt.title("Sand2BW")
#plt.xlabel("Inch")
#plt.ylabel("Inch")           
#plt.show()
#plt.close
"""
"""
- Loop through each frame of a given test
- Loop through different tests (start with only one test)
- Ensure that the code can find the center of the crater. Currently only works for a symmetric dataset
"""