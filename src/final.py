import preparation
import cv2
from roi_coordinates import coordinates_and_dimensions

def motion_detection():
    args = preparation.argument_parser()

    # Getting ROI and getting video object
    vs, roi_x, roi_y, roi_width, roi_height = roi_and_getting_object()

    # Initializing pygame with tone
    preparation.init_pygame("alarm.wav")

    # Initializing previous frame
    previous_frame = None
    looping_through_frames(vs, roi_x, roi_y, roi_width, roi_height, previous_frame)
    
    # Release the video capture and close windows
    vs.stop() if args == "webcam" else vs.release()
    cv2.destroyAllWindows()
    print("Completed, for now")


def roi_and_getting_object():
    print("Select a region of interest using mouse.")

    # Get coordinates of ROI
    roi_x, roi_y, roi_width, roi_height = coordinates_and_dimensions()

    print("Region of interest selected.")

    # Get VideoObject
    args = preparation.argument_parser()
    vs = preparation.reading_file(args=args)

    return vs, roi_x, roi_y, roi_width, roi_height

def looping_through_frames(vs, roi_x, roi_y, roi_width, roi_height, previous_frame):
    frame = preparation.getting_frame(vs)
    #print(type(vs))
        
    # Getting ROI ready
    kernel = (21,21)
    blurred_roi = preparation.getting_roi_ready(frame, roi_x, roi_y, roi_width, roi_height, kernel)

    # Initialize previous_frame for the first frame
    if previous_frame is None:
        return looping_through_frames(vs, roi_x, roi_y, roi_width, roi_height, blurred_roi)

    thresh1 = 85
    thresh2 = 255
    contours, _ = preparation.finding_contour(previous_frame, blurred_roi, thresh1, thresh2)

    # Finding motion in ROI
    previous_area = None
    min_area = 500
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    preparation.contour(previous_area, contours, min_area, roi)

    # Show the resulting frame
    cv2.imshow("Motion Detection", frame)
        
    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return None
    
    return looping_through_frames(vs, roi_x, roi_y, roi_width, roi_height, blurred_roi)


if __name__ == "__main__":
    motion_detection()