import cv2
import imutils
from roi_webcam import roi_array
import pygame

# Initialising pygame to play alarm.wav
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")
pygame.mixer.music.set_volume(50.0)

# Define the top-left and bottom-right coordinates of the ROI
roi_top_left = roi_array('1')[0]
roi_bottom_right =  roi_array('1')[0]

# Initialize the first frame and the status of motion
previous_frame = None
motion_detected = False

# Initialize the video capture
video_capture = cv2.VideoCapture(0)  # Replace 0 with the index of your webcam if you have multiple cameras

while True:
    # Read the current frame from the video capture
    ret, frame = video_capture.read()

    # Resize the frame for faster processing (optional)
    frame = imutils.resize(frame, width=500)

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
    threshold = cv2.threshold(frame_delta, 75, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in holes
    threshold = cv2.dilate(threshold, None, iterations=2)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any motion is detected in the ROI
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

            # Calculate the bounding rectangle of the contour
        (x, y, w, h) = cv2.boundingRect(contour)
            
            
            # Calculate the area of the contour
        current_area = w * h

            # Check if there is motion inside the bounding rectangle
        if previous_area is None:
                # Update the previous area
            previous_area = current_area
            
        if current_area > previous_area:
                break
            # Draw a bounding box around the region of motion
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
        pygame.mixer.music.play()
    cv2.imshow("Motion Detection",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
video_capture.release()
cv2.destroyAllWindows()



'''for contour in contours:
        # If the contour is too small, ignore it
        if cv2.contourArea(contour) < 10000:
            continue

        # Compute the bounding box coordinates
        (x, y, w, h) = cv2.boundingRect(contour)

        # Check if the bounding box is within the ROI
        if roi_top_left[0] < x < roi_bottom_right[0] and roi_top_left[1] < y < roi_bottom_right[1]:
            # Motion detected within the ROI
            motion_detected = True
            motion_status = "Motion Detected"
            pygame.mixer.music.play()
            break
            

    # Draw the ROI rectangle on the frame
    cv2.rectangle(frame, roi_top_left, roi_bottom_right, (0, 255, 0), 2)

    # Draw the motion status on the frame
    cv2.putText(frame, motion_status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Show the processed frame
    cv2.imshow("Motion Detection", frame)

    # Wait for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()'''
