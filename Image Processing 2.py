# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:00:27 2023

@author: Sudan Devkota
"""

import cv2
import numpy as np

# Load the image
image_path = r'C:\Users\Sudan Devkota\Downloads\T3.png'
image = cv2.imread(image_path)

# Define ROI coordinates (top-left and bottom-right)
roi_tl = (350, 249)  # Example top-left corner (x, y)
roi_br = (1711, 1034)  # Example bottom-right corner (x, y)

# Crop the image to the ROI
roi_image = image[roi_tl[1]:roi_br[1], roi_tl[0]:roi_br[0]]

# Convert the ROI image to grayscale
gray = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and enhance features
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny edge detection to find edges
edges = cv2.Canny(blurred, threshold1=30, threshold2=70)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop through the detected contours
for contour in contours:
    # Fit a curve to the contour using polynomial approximation
    if len(contour) > 5:
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

# Display the image with detected parabolic curves in the ROI
cv2.imshow("Detected Parabolic Curves in ROI", roi_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

