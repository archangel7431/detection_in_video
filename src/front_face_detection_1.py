import cv2
import argparse
from imutils.video import VideoStream
import time
import pygame
from roi_coordinates import coordinates_and_dimensions
from roi import roi

# Initialising pygame to play alarm.wav
pygame.mixer.init()
pygame.mixer.music.load("alarm.wav")
pygame.mixer.music.set_volume(50.0)

# Load the pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int,
                default=500, help="minimum area size")
args = vars(ap.parse_args())

# Get coordinates and dimensions of ROI
roi = roi()
roi_x, roi_y, roi_width, roi_height = coordinates_and_dimensions(roi=roi)

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    vs = cv2.VideoCapture(args["video"])

# Initializing previous frame
previous_frame = None

while True:
    if args.get("video", None) is None:
        frame = vs.read()
    else:
        ret, frame = vs.read()
        if not ret:
            break

    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred_roi = cv2.GaussianBlur(gray_roi, (31, 31), 0)

    if previous_frame is None:
        previous_frame = blurred_roi
        continue

    frame_delta = cv2.absdiff(previous_frame, blurred_roi)
    thresh = cv2.threshold(frame_delta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    contours, _ = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    previous_area = None

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        current_area = w * h

        if previous_area is None:
            previous_area = current_area

        if current_area > previous_area:
            break

        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
        pygame.mixer.music.play()

        # Detect faces in the grayscale ROI
        faces = face_cascade.detectMultiScale(
            gray_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Iterate over the detected faces and draw rectangles around them
        for (fx, fy, fw, fh) in faces:
            cv2.rectangle(roi, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
            pygame.mixer.music.play()

        previous_area = current_area

    cv2.imshow("Motion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
