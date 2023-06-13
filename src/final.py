import preparation
from roi_coordinates import coordinates_and_dimensions


def roi_and_getting_object():
    print("Select a region of interest using mouse.")

    # Get coordinates of ROI
    roi_x, roi_y, roi_width, roi_height = coordinates_and_dimensions()

    print("Region of interest selected.")

    # Initialize pygame
    preparation.init_pygame("alarm.wav")

    # Get VideoObject
    args = preparation.argument_parser()
    vs = preparation.reading_file(args=args)

    print("completed")
    return vs

def looping_through_frames(vs):
    # Initializing previous frame
    previous_frame = None

    while True:
        if str(type(vs)) == "<class 'imutils.video.webcamvideostream.WebcamVideoStream'>":
            frame = vs.read()
        elif str(type(vs)) == "<class 'cv2.VideoCapture'>":
            ret, frame = vs.read()
            # If there is no frame to read anymore, then break
            if not ret:
                break

        print(type(frame))
        
        break

if __name__ == "__main__":
    vs = roi_and_getting_object()
    looping_through_frames(vs=vs)