import os
#import cv2

dir = os.listdir()
search = [".mp4"]
search.append(input("Search term: "))
for i in range(len(search)):
    search[i] = search[i].lower()
print(search)

#find a .mp4 in the current directory
for i in dir:
    if all([x in i for x in search]):
        #vid = cv2.VideoCapture(i)
        file = i[:-4:]
        break
    elif i == dir[len(dir)-1]:
        file = "NotFound"
        raise SystemExit("File not found.")

print("File = " + file)
