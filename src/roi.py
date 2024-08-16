import cv2
import argparse
import os


# Callback function for mouse events
def select_roi(event, x, y, flags, param):
    global roi_top_left, roi_bottom_right, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_top_left = (x, y)
        roi_selected = False

    elif event == cv2.EVENT_LBUTTONUP:
        roi_bottom_right = (x, y)
        roi_selected = True


def get_roi(vs):
    """
    Returns the region of interest (ROI) selected by the user from the video object.
    Args:
    vs: cv2.VideoCapture - The video object.

    Returns:
    list - The top left and bottom right coordinates of the ROI.
    """

    global roi_top_left, roi_bottom_right, roi_selected

    # Initialize variables
    roi_top_left = None
    roi_bottom_right = None
    roi_selected = False

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", select_roi)

    while True:
        # Read the current frame from the video capture
        _, frame = vs.read()

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

    return [roi_top_left, roi_bottom_right]


def roi(source: str) -> list:
    """
    Returns the region of interest (ROI) selected by the user.
    Args:
    source: str - The source of the video.

    Returns:
    list - The top left and bottom right coordinates of the ROI.
    """

    # Check if the source is a valid path or webcam. If not, print an error message.
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

    return get_roi(vs)


if __name__ == "__main__":
    source = "./src/res/video_1.mp4"
    roi(source)
