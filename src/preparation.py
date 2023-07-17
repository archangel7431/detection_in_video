# Importing libraries
import cv2
import argparse
import os
import numpy as np
from roi_coordinates import coordinates_and_dimensions
import platform


def argument_parser():
    # Construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode", help="Type 'webcam' for webcam or if the source is a video file, write its path.")
    args = parser.parse_args()

    return args.mode


# Reading file/ webcam
def reading_file(args):
    # if the video argument is None, then we are reading from webcam
    if args == "webcam":
        vs = cv2.VideoCapture(0)

    # Otherwise, we are reading from a video file
    else:
        if os.path.exists(args):
            vs = cv2.VideoCapture(args)
        else:
            print(
                f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}. Try writing a path relative to the program.")

    return vs


def getting_roi_ready(frame, roi_wanted, coordinates):
    if not roi_wanted:
        roi = frame
    else:
        roi_x, roi_y, roi_width, roi_height = coordinates
        # Crop the frame to the ROI
        roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

        # Displaying rectangle representing roi in the frame
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width,
                      roi_y + roi_height), (0, 255, 0), 2)

    return roi


def finding_contour(fgmask, thresh):

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(fgmask, thresh, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    kernel = np.ones((7, 7), np.uint8)
    thresh = cv2.erode(thresh, kernel=kernel)
    thresh = cv2.dilate(thresh, None, iterations=6)

    # Find contours of the thresholded image
    contours = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return contours


def contour(contours, min_area, roi):
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            # Calculate the bounding rectangle of the contour
            (x, y, w, h) = cv2.boundingRect(contour)

            # Draw a bounding box around the region of motion
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)
            sound_alarm()


def sound_alarm():
    tone_path = "alarm.wav"
    import pygame
    pygame.mixer.init()
    if os.path.exists(tone_path):
        pygame.mixer.music.load(tone_path)
    else:
        print(
            f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}.")
    pygame.mixer.music.load(tone_path)
    pygame.mixer.music.set_volume(50.0)
    pygame.mixer.music.play()


if __name__ == "__main__":
    sound_alarm()
