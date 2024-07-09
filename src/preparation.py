# Importing libraries
import os
import argparse
import cv2
import numpy as np


def argument_parser():
    """
    Returns the mode argument from the command line.
    """
    # Construct the argument parser and parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        help=f"Type 'webcam' for webcam or if the source is a video file, write its path. Current directory is {os.path.abspath(__file__)}.",
    )
    args = parser.parse_args()

    return args.mode


# Reading file/ webcam
def reading_file(client):
    """
    Reads the video file or webcam.
    Args:
    client: tuple - contains whether we require command line interface or client interface
                    and the file path (file path is None if command line interface is required).

    Returns:
    vs: cv2.VideoCapture - The video object."""

    file_path = client[1]
    if client[0] and os.path.exists(file_path):
        vs = cv2.VideoCapture(file_path)
        return vs

    # client[0] is False, which means command line interface is required
    elif not client[0]:
        args = argument_parser()

        # if the video argument is None, then we are reading from webcam
        if args == "webcam":
            vs = cv2.VideoCapture(0)

        # Otherwise, we are reading from a video file
        if os.path.exists(args):
            vs = cv2.VideoCapture(args)
        else:
            print(
                f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}. Try writing a path relative to the program."
            )

        return vs


def getting_roi_ready(frame, roi_wanted, coordinates):
    """
    Returns the region of interest (ROI) from the frame.

    Args:
    frame: np.ndarray - The frame from which the ROI is to be extracted.
    roi_wanted: bool - If True, the ROI is to be extracted. If False, the whole frame is returned.
    coordinates: tuple - The coordinates of the ROI.

    Returns:
    roi: np.ndarray - The region of interest.
    """
    if not roi_wanted:
        roi = frame
    else:
        roi_x, roi_y, roi_width, roi_height = coordinates
        # Crop the frame to the ROI
        roi = frame[roi_y : roi_y + roi_height, roi_x : roi_x + roi_width]

        # Displaying rectangle representing roi in the frame
        cv2.rectangle(
            frame,
            (roi_x, roi_y),
            (roi_x + roi_width, roi_y + roi_height),
            (0, 255, 0),
            2,
        )

    return roi


def finding_contour(fgmask, thresh):
    """
    Returns the contours of the thresholded image.
    Args:
    fgmask: np.ndarray - The thresholded image.
    thresh: int - The threshold value.

    Returns:
    contours: list - The contours of the thresholded image.
    """

    # Apply a threshold to extract regions of significant motion
    thresh = cv2.threshold(fgmask, thresh, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to remove noise and fill holes
    kernel = np.ones((7, 7), np.uint8)
    thresh = cv2.erode(thresh, kernel=kernel)
    thresh = cv2.dilate(thresh, None, iterations=6)

    # Find contours of the thresholded image
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    return contours


def contour(contours, min_area, roi):
    """
    Draws a bounding box around the region of motion.
    Args:
    contours: list - The contours of the thresholded image.
    min_area: int - The minimum area of the contour to be considered as motion.
    roi: np.ndarray - The region of interest.

    Returns:
    None
    """
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            # Calculate the bounding rectangle of the contour
            (x, y, w, h) = cv2.boundingRect(contour)

            # Draw a bounding box around the region of motion
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 3)
            sound_alarm()


def sound_alarm():
    """
    Plays an alarm sound when motion is detected.
    """
    tone_path = "alarm.wav"
    import pygame

    pygame.mixer.init()
    if os.path.exists(tone_path):
        pygame.mixer.music.load(tone_path)
    else:
        print(
            f"Enter a valid path on this computer. This program is running from {os.path.abspath(__file__)}."
        )
    pygame.mixer.music.load(tone_path)
    pygame.mixer.music.set_volume(50.0)
    pygame.mixer.music.play()


if __name__ == "__main__":
    sound_alarm()
