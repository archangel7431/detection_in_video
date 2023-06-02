import cv2

def gaussian_blur(path:str):
    # Opening a video file and video capturing function
    video = cv2.VideoCapture(path)

    # Frame
    current_frame = 0

    # Frame sampling rate
    sampling_rate = 60  # Extract every 60th frame

    # Gaussian blur kernel size
    kernel_size = (101, 51)  # Adjust the kernel size as needed

    while True:
    # Reading from frame
        ret, frame = video.read()

        if ret:
            # If video is still left and the current frame is a multiple of the sampling rate, create an image
            if current_frame % sampling_rate == 0:
                   
                name = './src/res/video_1/gaussian_blur/frame' + str(current_frame) + '.jpg'
                
                # Convert frame to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian blur to smoothen the frame
                blurred_frame = cv2.GaussianBlur(gray_frame, kernel_size, 0)

                # Saving the extracted and smoothened grayscale image
                cv2.imwrite(name, blurred_frame)

            current_frame += 1
        else:
                break

    # Release all space and windows once done
    video.release()
    cv2.destroyAllWindows()

    return blurred_frame

# first frame blurred
def first_frame(webcam = False):

    if webcam:
        video = cv2.VideoCapture(0)
        name = "./src/webcam/gauusain_blur/frame0.jpg"

    else:
        path = input("Enter the video file path: ")
        video = cv2.VideoCapture(path)
        name = "./src/res/video_1/gaussian_blur/frame0.jpg"

    # Gaussian blur kernel size
    kernel_size = (101, 51)  # Adjust the kernel size as needed

    # Reading from frame
    ret, frame = video.read()

    # For the first frame
    if ret:        
        # convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to smoothen the frame
        blurred_frame = cv2.GaussianBlur(gray_frame, kernel_size, 0)

        # Saving the extracted and smoothened grayscale image
        cv2.imwrite(name, blurred_frame)
        print(f"creating {name}") 
  


if __name__ == "__main__":
    path='./src/res/video_1.mp4' 
    blurred_frame =first_frame(path)
    print(blurred_frame)