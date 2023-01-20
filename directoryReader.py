import os

dir = os.listdir()

for i in dir:
    if ".mp4" in i:

        print(i.rstrip(i[-1]))