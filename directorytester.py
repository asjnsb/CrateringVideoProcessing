import os

absPath = os.path.dirname(__file__)
head, tail = os.path.split(absPath)
while "Users" not in os.path.basename(head):
    head, tail = os.path.split(head)

path = os.path.join(head, tail, "Videos", "CrateringVideos")

if not os.path.exists(path):
    os.makedirs(path)
    print("Created", path)
else:
    print("Already here!")

#https://docs.python.org/3/library/os.path.html for docs: os.path.join os.path.relpath os.path.split should be useful
#NEXT: split works great, just keep working