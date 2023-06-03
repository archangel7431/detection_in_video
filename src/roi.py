import cv2

# Callback function for mouse events
def select_roi(event, x, y, flags, param):
    global roi_top_left, roi_bottom_right, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_top_left = (x, y)
        roi_selected = False

    elif event == cv2.EVENT_LBUTTONUP:
        roi_bottom_right = (x, y)
        roi_selected = True

def roi():
    global roi_top_left, roi_bottom_right, roi_selected

    # Initialize variables
    roi_top_left = None
    roi_bottom_right = None
    roi_selected = False

    # Prompt the user to choose between webcam and video file
    source_choice = input("Select the source: (1) Webcam (2) Video File: ")
    if source_choice == "1":
        # Start capturing video from the webcam
        video_capture = cv2.VideoCapture(0)  # Replace 0 with the index of your webcam if you have multiple cameras

    elif source_choice == "2":
        # Prompt the user for the video file path
        video_file = input("Enter the video file path: ")
        video_capture = cv2.VideoCapture(video_file)

    else:
        print("Invalid choice. Exiting.")
        exit()

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", select_roi)

    # Initialize variables for motion detection
    previous_frame = None
    motion_detected = False

    while True:
        # Read the current frame from the video capture
        ret, frame = video_capture.read()

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