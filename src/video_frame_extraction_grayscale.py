import cv2

# Opening a video file and video capturing function
video = cv2.VideoCapture('./res/video_1.mp4')

# Frame
current_frame = 0

# Frame sampling rate
sampling_rate = 60  # Extract every 60th frame

while True:
    # Reading from frame
    ret, frame = video.read()

    if ret:
        # If video is still left and the current frame is a multiple of the sampling rate, create an image
        if current_frame % sampling_rate == 0:
            name = './res/video_1/grayscale/frame' + str(current_frame) + '.jpg'
            print('Creating...' + name)

            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Saving the extracted grayscale image
            cv2.imwrite(name, gray_frame)

        current_frame += 1
    else:
        break

# Release all space and windows once done
video.release()
cv2.destroyAllWindows()
