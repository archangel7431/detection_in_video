# Import the required libraries
from roi import roi


def roi_corner_coordinates(roi):
    left_top_corner = roi[0]
    left_bottom_corner = (roi[0][0], roi[1][1])
    right_bottom_corner = roi[1]
    right_top_corner = (roi[1][0], roi[0][1])

    return left_top_corner, left_bottom_corner, right_bottom_corner, right_top_corner


def coordinates_and_dimensions(source: str) -> tuple:
    """
    This function is used to get the coordinates and dimensions of the region of interest (ROI).
    The user will select the ROI using the mouse.
    The function will then return the coordinates and dimensions of the ROI.

    Args:
    source: str - The source of the video.

    Returns:
    roi_x: int - The x-coordinate of the ROI.
    roi_y: int - The y-coordinate of the ROI.
    roi_width: int - The width of the ROI.
    roi_height: int - The height of the ROI.
    """
    roi_1 = roi(source)
    roi_x = roi_1[0][0]
    roi_y = roi_1[0][1]
    roi_width = abs(roi_1[0][0] - roi_1[1][0])
    roi_height = abs(roi_1[0][1] - roi_1[1][1])

    return roi_x, roi_y, roi_width, roi_height
