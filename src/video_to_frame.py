import cv2

#opening a video file and video capturing function
video=cv2.VideoCapture('./res/video_1.mp4')

#frame
currentframe=0

while(True):
    #reading from frame
    ret,frame=video.read()
    if ret:
        #if video is still left continue creating images
        name= './res/video/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        # saving the extracted images
        cv2.imwrite(name,frame)

        currentframe+= 1
    else:
        break


# release all space and windows once done.
video.release()
cv2.destroyAllWindows()