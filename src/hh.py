import cv2
import imutils
import pygame

# Callback function for mouse events
def select_roi(event, x, y, flags, param):
    global roi_top_left, roi_bottom_right, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_top_left = (x, y)
        roi_selected = False

    elif event == cv2.EVENT_LBUTTONUP:
        roi_bottom_right = (x, y)
        roi_selected = True

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

# Initialize pygame for playing the alarm sound
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")  # Replace "alarm.wav" with your own audio file

while True:
    # Read the current frame from the video capture
    ret, frame = video_capture.read()

    # Flip the frame horizontally (optional, depending on your camera setup)
    #frame = cv2.flip(frame, 1)

    # Resize the frame for faster processing (optional)
    #frame = imutils.resize(frame, width=500)

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

# Print the selected ROI coordinates
print("ROI Top Left: ", roi_top_left)
print("ROI Bottom Right: ", roi_bottom_right)

# Start capturing video again, this time for motion detection
if source_choice == "1":
    video_capture = cv2.VideoCapture(0)
else:
    video_capture = cv2.VideoCapture(video_file)

# Set the ROI coordinates
x1, y1 = roi_top_left
x2, y2 = roi_bottom_right

while True:
    # Read the current frame from the video capture
    ret, frame = video_capture.read()

    # Flip the frame horizontally (optional, depending on your camera setup)
    #frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise and improve accuracy
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize the motion status
    motion_status = "No Motion"

    # If it's the first frame, save it for reference and continue to the next frame
    if previous_frame is None:
        previous_frame = gray
        continue

    # Compute the absolute difference between the current frame and the previous frame
    frame_delta = cv2.absdiff(previous_frame, gray)

    # Apply a threshold to the frame delta
    threshold = cv2.threshold(frame_delta, 80, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes
    threshold = cv2.dilate(threshold, None, iterations=2)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any motion is detected in the ROI
    for contour in contours:
        # If the contour is too small, ignore it
        if cv2.contourArea(contour) < 500:
            continue

        # Compute the bounding box coordinates
        (x, y, w, h) = cv2.boundingRect(contour)

        # Check if the bounding box is within the ROI
        if x1 < x < x2 and y1 < y < y2:
            # Motion detected within the ROI
            motion_detected = True
            motion_status = "Motion Detected"
            break

    # Draw the ROI rectangle on the frame
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (0, 255, 0), 2)

    # Draw the motion status on the frame
    cv2.putText(frame, motion_status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Play the alarm sound if motion is detected
    if motion_detected:
        pygame.mixer.music.play(-1)  # Loop the alarm sound until motion is no longer detected
    else:
        pygame.mixer.music.stop()

    # Display the frame with motion status
    cv2.imshow("Motion Detection", frame)

    # Wait for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
