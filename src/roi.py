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


def argument_parser():
    # Construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        help="Type 'webcam' for webcam or if the source is a video file, write its path.",
    )
    args = parser.parse_args()

    return args.mode


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


def roi(client):
    """
    Returns the region of interest (ROI) selected by the user.
    Args:
    client: tuple - contains whether we require command line interface or client interface
                    and the file path (file path is None if command line interface is required).

    Returns:
    list - The top left and bottom right coordinates of the ROI.
    """

    filepath = client[1]

    # If client[0] is True and the file path exists, then we are reading
    # from a video file in the system and we are getting the ROI from the
    # video file.
    if client[0] and os.path.exists(filepath):
        vs = cv2.VideoCapture(filepath)
        return get_roi(vs)

    # If client[0] is False, then we are using command line interface.
    elif not client[0]:
        args = argument_parser()

        # If the video argument is None, then we are reading from webcam
        if args == "webcam":
            vs = cv2.VideoCapture(0)

        # Otherwise, we are reading from a video file
        if os.path.exists(args):
            vs = cv2.VideoCapture(args)
        else:
            print(
                f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}. Try writing a path relative to the program."
            )
        return get_roi(vs)


if __name__ == "__main__":
    print(roi((True, "src/res/video_1.mp4")))
