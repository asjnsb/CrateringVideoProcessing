import os

absPath = os.path.dirname(__file__)
head, tail = os.path.split(absPath)
while "Users" not in os.path.basename(head):
    head, tail = os.path.split(head)


print(head)

#https://docs.python.org/3/library/os.path.html for docs: os.path.join os.path.relpath os.path.split should be useful
#NEXT: split works great, just keep working