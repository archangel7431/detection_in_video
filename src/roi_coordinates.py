# Import the required libraries
import cv2
import numpy as np
from roi_array import roi_array

def roi_corner_coordinates(roi):
    left_top_corner = roi[0]
    left_bottom_corner = (roi[0][0], roi[1][1])
    right_bottom_corner = roi[1]
    right_top_corner = (roi[1][0], roi[0][1])
    
    return left_top_corner, left_bottom_corner, right_bottom_corner, right_top_corner

def coordinates_and_dimensions(roi):
    roi_x = roi[0][0]
    roi_y = roi[0][1]
    roi_width = abs(roi[0][0] - roi[1][0])
    roi_height = abs(roi[0][1] - roi[1][1])

    return roi_x, roi_y, roi_width, roi_height

if __name__ == "__main__":
    roi = roi_array("./src/res/video_1/gaussian_blur/frame60.jpg")
    left_top_corner, left_bottom_corner, right_bottom_corner, right_top_corner= roi_corner_coordinates(roi)
    print(f"Left Top Corner: {left_top_corner}")
    print(f"Left Bottom Corner: {left_bottom_corner}")
    print(f"Right Bottom Corner: {right_bottom_corner}")
    print(f"Right Top Corner: {right_top_corner}")
