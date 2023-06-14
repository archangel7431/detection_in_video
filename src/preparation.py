# Importing libraries
import cv2
import pygame
import argparse
from imutils.video import VideoStream 
import time
import os
from roi_coordinates import coordinates_and_dimensions


# Initialising pygame to play
def init_pygame(tone_path):
    pygame.mixer.init()
    pygame.mixer.music.load(tone_path)
    pygame.mixer.music.set_volume(50.0)


def argument_parser():
    # Construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help = "Type 'webcam' for webcam or if the source is a video file, write its path.")
    args = parser.parse_args()

    return args.mode


# Reading file/ webcam
def reading_file(args):
    # if the video argument is None, then we are reading from webcam
    if args == "webcam":
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        
    # Otherwise, we are reading from a video file
    else:
        if os.path.exists(args):
            vs= cv2.VideoCapture(args)
        else:
            print(f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}. Try writing a path relative to the program.")

    return vs  


def getting_frame(vs):
    if str(type(vs)) == "<class 'imutils.video.webcamvideostream.WebcamVideoStream'>":
            frame = vs.read()
    elif str(type(vs)) == "<class 'cv2.VideoCapture'>":
        ret, frame = vs.read()

    return frame


def getting_roi_ready(frame, roi_x, roi_y, roi_width, roi_height, kernel:tuple):

    # Crop the frame to the ROI
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
       
    # Displaying rectangle representing roi in the frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (0, 255, 0), 2)

   # Convert the ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_roi = cv2.GaussianBlur(gray_roi, kernel, 0)
    
    return blurred_roi


def finding_contour(previous_frame, blurred_roi, thresh1, thresh2):
    # Calculate the absolute difference between the current and previous frames
    frame_delta = cv2.absdiff(previous_frame, blurred_roi)

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(frame_delta, thresh1, thresh2, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, _


def contour(previous_area, contours, min_area, roi):
    for contour in contours:
        if cv2.contourArea(contour) < min_area:
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
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
        pygame.mixer.music.play()

if __name__ == "__main__":
    pass