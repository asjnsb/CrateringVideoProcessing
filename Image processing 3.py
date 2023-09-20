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
roi_width = roi_image.shape[1]
roi_height = roi_image.shape[0]

gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY) # Convert the ROI image to grayscale
blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Apply Gaussian blur to reduce noise and enhance features
edges = cv2.Canny(blurred, threshold1=30, threshold2=70) # Apply Canny edge detection to find edges

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # Find contours in the edge-detected image, and return all points (CHAIN_APPROX_NONE)
drawnContours = cv2.drawContours(roi_image, contours, -1, (0, 255, 0), 1) # Draw the contours (img, contours, which contour?, color, line width)
contourFile = open("CountourData.txt", "w") # create a file for outputing data

for contour in contours:
    #contourFile.write("%s\n"%contour)
    for point in contour:# point is a list containing a touple, so point[0] points directly to the tuple. point[1] DNE
        if point[0][0] == (roi_width/2) and point[0][1] > (roi_height/2): 
            print(point[0])
        

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

contourFile.close()
cv2.imshow("show contours", drawnContours)
"""# Display the image with detected parabolic curves in the ROI
#cv2.imshow("Detected Parabolic Curves in ROI", roi_image)"""
cv2.waitKey(0)
cv2.destroyAllWindows()

#LAST: can find points below the center point
#NEXT: need to correlate a found point to a contour to isolate it from the rest of the contours.