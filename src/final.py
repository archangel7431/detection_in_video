import cv2
import preparation
from roi_coordinates import coordinates_and_dimensions


def motion_detection(client=None, filepath=None):
    """
    This function is used to detect motion in a video file or from a webcam.
    It uses the MOG2 background subtraction algorithm to detect motion in the
    region of interest (ROI) and then draws a rectangle around the detected
    motion. The user can select a region of interest using the mouse. The
    program will then display the video with the detected motion highlighted
    by a red rectangle. The program will continue to run until the user
    presses the 'q' key or closes the window. The program will then release
    the video capture and close the windows.

    :param client: If the function is called from the client, the client
    argument will be passed and command line will be turned off. If the
    function is called from the command line, the client argument will not be
    passed and the command line will be turned on.
    """
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Getting ROI and getting video object
    roi_wanted = bool(
        input("If you don't want ROI, press ENTER. If you want ROI, write 'True': ")
    )

    vs, coordinates = roi_and_getting_object(
        client=client, file_path=filepath, roi_wanted=roi_wanted
    )

    while True:
        _, frame = vs.read()
        roi = preparation.getting_roi_ready(frame, roi_wanted, coordinates)
        fgmask = fgbg.apply(roi)

        thresh = 85
        contours = preparation.finding_contour(fgmask, thresh)

        # Finding motion in ROI
        min_area = 500

        preparation.contour(contours, min_area, roi=roi)

        # Show the resulting frame
        cv2.imshow("Motion Detection", frame)

        # Break the loop on 'q' key press or if the window was closed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        try:
            # Try to get ththe window property
            cv2.getWindowProperty("Motion Detection", 0)
        except cv2.error:
            # If an error is caught, it means the window has been closed
            break

    # Release the video capture and close windows
    vs.release()
    cv2.destroyAllWindows()
    print("Completed, for now")


def roi_and_getting_object(client=None, file_path=None, roi_wanted=True):
    # Command line interface
    if not client:
        # ROI Not wanted
        if not roi_wanted:
            # Get VideoObject
            args = preparation.argument_parser()
            vs = preparation.reading_file(args=args)
            coordinates = ()

        # ROI wanted
        else:
            print("Select a region of interest using mouse.")

            # Get coordinates of ROI
            coordinates = tuple(coordinates_and_dimensions())

            print("Region of interest selected.")

            # Get VideoObject
            args = preparation.argument_parser()
            vs = preparation.reading_file(args=args)

    # folder path
    else:
        if not roi_wanted:
            vs = preparation.reading_file(client=client, file_path=file_path)
            coordinates = ()

        else:
            print("Select a region of interest using mouse.")

            # Get coordinates of ROI
            coordinates = tuple(coordinates_and_dimensions())

            print("Region of interest selected.")

            # Get VideoObject
            vs = preparation.reading_file(client=client, file_path=file_path)

    return vs, coordinates


if __name__ == "__main__":
    motion_detection()
