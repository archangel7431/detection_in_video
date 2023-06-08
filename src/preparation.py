# Importing libraries
import cv2
import pygame
import argparse
from imutils.video import VideoStream 
import time


# Initialising pygame to play
def init_pygame(tone_path):
    pygame.mixer.init()
    pygame.mixer.music.load(tone_path)
    pygame.mixer.music.set_volume(50.0)


def argument_parser():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help = "path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    return args


# Reading file/ webcam
def reading_file(args):
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        
    # Otherwise, we are reading from a video file
    else:
        vs= cv2.VideoCapture(args["video"])

    return vs  