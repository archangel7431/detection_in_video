import cv2
from roi_coordinates import coordinates_and_dimensions
from roi_array import roi_array
import pygame

# Initialising pygame to play alarm.wav
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")
pygame.mixer.music.set_volume(50.0)


# From path of a frame, we're finding the coordinates and dimensions of ROI(Region of Interest)
roi = roi_array("./src/res/video_1/gaussian_blur/frame180.jpg")
roi_x, roi_y, roi_width, roi_height = coordinates_and_dimensions(roi)

# Initializing previous frame
previous_frame = None

# Opening video file
cap = cv2.VideoCapture("./src/res/video_1.mp4")  

while True:
    # Reading the VideoObject
    ret, frame = cap.read()

    # If there is no frame to read anymore, then break
    if not ret:
        break

    # Crop the frame to the ROI
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_roi = cv2.GaussianBlur(gray_roi, (21, 21), 0)

    # Initialize previous_frame for the first frame
    if previous_frame is None:
        previous_frame = blurred_roi
        continue

    # Calculate the absolute difference between the current and previous frames
    frame_delta = cv2.absdiff(previous_frame, blurred_roi)

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(frame_delta, 75, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    previous_area = None

    # Iterate over the contours and filter out small contours
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

    # Show the resulting frame
    cv2.imshow("Motion Detection", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()