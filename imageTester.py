import cv2
import numpy as np

# Load the image
image_path = r'C:/Users/asjns/Videos/CrateringVideos/T15_LHS1_240fps_4-28-23_Frames_fSkip20/T15_LHS1_240fps_4-28-23_frame07760.png'

image = cv2.imread(image_path)
print(image.shape[1])
print(image.shape[0])