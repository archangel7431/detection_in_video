import preparation
import cv2
from roi_coordinates import coordinates_and_dimensions


def motion_detection(command_line=True):
    if command_line:
        preparation.argument_parser()
    else:
        pass

    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Getting ROI and getting video object
    roi_wanted = bool(
        input("If you don't want ROI, press ENTER. If you want ROI, write 'True': "))
    vs, coordinates = roi_and_getting_object(roi_wanted)

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

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture and close windows
    vs.release()
    cv2.destroyAllWindows()
    print("Completed, for now")


def roi_and_getting_object(roi_wanted):
    if not roi_wanted:
        # Get VideoObject
        args = preparation.argument_parser()
        vs = preparation.reading_file(args=args)
        coordinates = ()

        return vs, coordinates

    else:
        print("Select a region of interest using mouse.")

        # Get coordinates of ROI
        coordinates = tuple(coordinates_and_dimensions())

        print("Region of interest selected.")

        # Get VideoObject
        args = preparation.argument_parser()
        vs = preparation.reading_file(args=args)

        return vs, coordinates


if __name__ == "__main__":
    motion_detection()
