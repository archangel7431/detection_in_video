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
    parser.add_argument("mode", help = "Type 'webcam' for webcam or if the source is a video file, write its path.")
    args = parser.parse_args()

    return args.mode

def roi():
    global roi_top_left, roi_bottom_right, roi_selected

    # Initialize variables
    roi_top_left = None
    roi_bottom_right = None
    roi_selected = False

    # Prompt the user to choose between webcam and video file
    args = argument_parser()
    source_choice = str(args)
    if source_choice == "webcam":
        # Start capturing video from the webcam
        video_capture = cv2.VideoCapture(0)  # Replace 0 with the index of your webcam if you have multiple cameras

    else:
        if os.path.exists(args):
            video_capture = cv2.VideoCapture(source_choice)
        else:
            print(f"Enter a valid path on this computer. \
                  This program is running from {os.path.abspath(__file__)}. \
                  Try writing a path relative to the program.")

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", select_roi)


    while True:
        # Read the current frame from the video capture
        _, frame = video_capture.read()

        # Display the frame
        cv2.imshow("Select ROI", frame)

        # Break the loop if ROI has been selected
        if roi_selected:
            break

        # Wait for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

    return [roi_top_left, roi_bottom_right]


if __name__ == "__main__":
    print(roi())