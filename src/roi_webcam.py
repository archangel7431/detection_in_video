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



def roi_array(source_choice : str,):
    global roi_selected, roi_bottom_right, roi_top_left

    # Initialize variables
    roi_top_left = None
    roi_bottom_right = None
    roi_selected = False


    if source_choice == "1":
        # Start capturing video from the webcam
        video_capture = cv2.VideoCapture(0)
    
    elif source_choice == "2":
        video_file = input("Enter the video file path: ")
        video_capture = cv2.VideoCapture(video_file)
    
    else:
        print("Invalid choice. Exiting...")
        exit()

    # Create a window and bind the mouse callback function
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", select_roi)

    while True:
        # Read the current frame from the video capture
        ret, frame = video_capture.read()

        if not ret:
            break

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
    source_choice = input("Enter the source_choice(1 for webcam and 2 for video file): ")
    roi_pts = roi_array(source_choice=source_choice)
    print(roi_pts)