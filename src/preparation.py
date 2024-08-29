# Importing libraries
import os
import cv2
import numpy as np


# Reading file/ webcam
def reading_file(source: str) -> cv2.VideoCapture:
    """
    Reads the video file or webcam.

    Args:
    source: str - The source of the video.

    Returns:
    vs: cv2.VideoCapture - The video object.
    """

    # Check if the source is a webcam or a file. If not, print an error message.
    if source == "webcam":
        try:
            vs = cv2.VideoCapture(0)
        except cv2.error:
            print("Webcam not found. Please check the connection.")
    elif os.path.exists(source):
        try:
            vs = cv2.VideoCapture(source)
        except cv2.error:
            print("Enter a valid path.")
            print(f"This program is running from {os.path.abspath(__file__)}.")
    else:
        print("Enter a valid path on this computer or 'webcam'.")

    return vs


# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    """
    This function is a callback function that is called when the mouse is used to draw a rectangle.
    It is used to draw a rectangle on the frame.

    Args:
    event: int - The event that is triggered.
    x: int - The x-coordinate of the mouse pointer.
    y: int - The y-coordinate of the mouse pointer.
    flags: int - The flags that are set.
    param: int - The parameters that are passed.

    Returns:
    None
    """
    global ix, iy, roi_selected, drawing, top_left_x, top_left_y, width, height

    # If the left mouse button is pressed, start drawing the rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True  # Set the drawing flag to True. Means drawing has started.
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False  # Set the drawing flag to False. Means drawing has stopped.
        roi_selected = (
            True  # Set the ROI selected flag to True. Means ROI has been selected.
        )

        # Setting ROI coordinates
        top_left_x = min(ix, x)
        top_left_y = min(iy, y)
        bottom_right_x = max(ix, x)
        bottom_right_y = max(iy, y)

        # Calculating width and height of the ROI
        width = bottom_right_x - top_left_x
        height = bottom_right_y - top_left_y


# Getting ROI coordinates
def get_roi_coordinates(source: str) -> tuple:
    """
    This function is used to get the coordinates of the region of interest (ROI).
    The user will select the ROI using the mouse.
    The function will then return the coordinates of the ROI as a tuple.

    Args:
    source: str - The source of the video.

    Returns:
    coordinates: tuple - The coordinates of the ROI.
    """

    global ix, iy, roi_selected, drawing, top_left_x, top_left_y, width, height

    # Initialize variables
    ix, iy = -1, -1  # Coordinates of the top left corner of the ROI
    roi_selected = False  # Flag to check if ROI has been selected
    drawing = False  # Flag to check if drawing has started

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", draw_rectangle)

    # Read the video file or webcam
    if os.path.exists(source):
        try:
            vs = cv2.VideoCapture(source)
        except cv2.error:
            print("Enter a valid path.")
            print(f"This program is running from {os.path.abspath(__file__)}.")
    elif source == "webcam":
        try:
            vs = cv2.VideoCapture(0)
        except cv2.error:
            print("Webcam not found. Please connect a webcam and try again.")
    else:
        print("Enter a valid path or 'webcam'.")

    while True:
        ret, frame = vs.read()
        if not ret:
            print("Could not read frame from video")
            break

        # Display the frame
        cv2.imshow("Select ROI", frame)

        # Break the loop if ROI has been selected
        if roi_selected:
            break

        # Wait for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the video capture and close all windows
    vs.release()
    cv2.destroyAllWindows()

    coordinates = (top_left_x, top_left_y, width, height)

    return coordinates


# Getting ROI ready
def getting_roi_ready(
    frame: np.ndarray, roi_wanted: bool, coordinates: tuple
) -> np.ndarray:
    """
    Returns the region of interest (ROI) from the frame.

    Args:
    frame: np.ndarray - The frame from which the ROI is to be extracted.
    roi_wanted: bool - If True, the ROI is to be extracted. If False, the whole frame is returned.
    coordinates: tuple - The coordinates of the ROI.

    Returns:
    roi: np.ndarray - The region of interest.
    """
    if not roi_wanted:
        roi = frame
    else:
        roi_x, roi_y, roi_width, roi_height = coordinates
        # Crop the frame to the ROI
        roi = frame[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]

        # Displaying rectangle representing roi in the frame
        cv2.rectangle(
            frame,
            (roi_x, roi_y),
            (roi_x + roi_width, roi_y + roi_height),
            (0, 255, 0),
            2,
        )

    return roi


# Finding contours
def finding_contour(fgmask: np.ndarray, thresh: int) -> list:
    """
    Returns the contours of the thresholded image.
    Args:
    fgmask: np.ndarray - The thresholded image.
    thresh: int - The threshold value.

    Returns:
    contours: list - The contours of the thresholded image.
    """

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(fgmask, thresh, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    kernel = np.ones((7, 7), np.uint8)
    thresh = cv2.erode(thresh, kernel=kernel)
    thresh = cv2.dilate(thresh, None, iterations=6)

    # Find contours of the thresholded image
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return contours


# Drawing bounding box around the region of motion
def contour(contours: list, min_area: int, roi: np.ndarray) -> None:
    """
    Draws a bounding box around the region of motion.
    Args:
    contours: list - The contours of the thresholded image.
    min_area: int - The minimum area of the contour to be considered as motion.
    roi: np.ndarray - The region of interest.

    Returns:
    None
    """
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            # Calculate the bounding rectangle of the contour
            (x, y, w, h) = cv2.boundingRect(contour)

            # Draw a bounding box around the region of motion
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)
            sound_alarm()


# Sound alarm
def sound_alarm():
    """
    Plays an alarm sound when motion is detected.
    """
    tone_path = "alarm.wav"
    import pygame

    pygame.mixer.init()
    try:
        pygame.mixer.music.load(tone_path)
    except pygame.error:
        print(f"Enter a valid path.")

    pygame.mixer.music.set_volume(50.0)
    pygame.mixer.music.play()


if __name__ == "__main__":
    source = "src/res/video_1.mp4"
    get_roi_coordinates(source)
