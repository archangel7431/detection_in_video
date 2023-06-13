# Importing libraries
import cv2
import pygame
import argparse
from imutils.video import VideoStream 
import time
import os


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

if __name__ == "__main__":
    args = argument_parser()
    print(reading_file(args))