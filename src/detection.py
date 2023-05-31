# Importing libraries
import cv2
import numpy as np
import roi_array


# Define ROI Coordinates
roi = roi_array.roi_array("./src/res/video_1/gaussian_blur/frame60.jpg")
edge_coordinates = roi_array.roi_array(roi)
print(edge_coordinates)