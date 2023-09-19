# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:39:04 2023

@author: Sudan Devkota
@editor: Aidan St. John Sep 19 2023 +
"""

import cv2
import numpy as np

#=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=
# Parameters for cropping the image
centerXOff = 75
centerYOff = -75
vCrop = 0.3
hCrop = 0.3
#=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=^=

# Load the image
image_path = r'C:/Users/asjns/Videos/CrateringVideos/T16_LHS1_240fps_5-5-23_Frames_fSkip20/T16_LHS1_240fps_5-5-23_frame05360.png'
image = cv2.imread(image_path)

#Find the size of the image:
width = image.shape[1]
height = image.shape[0]

# Define ROI coordinates (top-left and bottom-right)
roi_tl = (int(width*hCrop)+centerXOff, int(height*vCrop)+centerYOff)  # Example top-left corner (x, y)
roi_br = (int(width*(1-hCrop))+centerXOff, int(height*(1-vCrop))+centerYOff)  # Example bottom-right corner (x, y)

# Crop the image to the ROI
roi_image = image[roi_tl[1]:roi_br[1], roi_tl[0]:roi_br[0]]

# Convert the ROI image to grayscale
gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and enhance features
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection to find edges
edges = cv2.Canny(blurred, threshold1=30, threshold2=70)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
drawnContours = cv2.drawContours(roi_image, contours, -1, (0, 255, 0), 1)
contourFile = open("CountourData.txt", "w")
for contour in contours:
    contourFile.write("%s\n"%contour)
"""
# Define the y-coordinate threshold for excluding contours below it
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

print("%s, %s" %(x, y))
"""
contourFile.close()
cv2.imshow("show contours", drawnContours)
#cv2.imshow("raw contours", edges)
# Display the image with detected parabolic curves in the ROI
#cv2.imshow("Detected Parabolic Curves in ROI", roi_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#LAST: simplified the code to find just the contours
#NEXT: develop a method for picking out the contour we want