import cv2
import numpy as np

def find_contours(previous_frame, blurred_roi):

    # Calculate the absolute difference between the current and previous frames
    frame_delta = cv2.absdiff(previous_frame, blurred_roi)

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(frame_delta, 35, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours