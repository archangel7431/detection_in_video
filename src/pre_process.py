# Import libraries
import cv2
import numpy as np

def pre_processing(frame, roi, roi_x, roi_y, roi_height, roi_width):
    # Crop the frame to the ROI
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_roi = cv2.GaussianBlur(gray_roi, (21, 21), 0)

    return blurred_roi