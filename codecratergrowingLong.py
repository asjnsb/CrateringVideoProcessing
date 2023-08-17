#!/usr/bin/python

import math
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("SetA1HOOSH.csv", delimiter=',', skiprows=1, unpack=True)
#data = np.loadtxt("datacratergrowingfull6.csv", delimiter=',', skiprows=1, unpack=True)

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
