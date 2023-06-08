# Import the required libraries
from roi import roi

def roi_corner_coordinates(roi):
    left_top_corner = roi[0]
    left_bottom_corner = (roi[0][0], roi[1][1])
    right_bottom_corner = roi[1]
    right_top_corner = (roi[1][0], roi[0][1])
    
    return left_top_corner, left_bottom_corner, right_bottom_corner, right_top_corner


def coordinates_and_dimensions():
    roi_1 = roi()
    roi_x = roi_1[0][0]
    roi_y = roi_1[0][1]
    roi_width = abs(roi_1[0][0] - roi_1[1][0])
    roi_height = abs(roi_1[0][1] - roi_1[1][1])

    return roi_x, roi_y, roi_width, roi_height