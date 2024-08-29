import cv2
import argparse

import preparation


def motion_detection(
    source: str,
    roi_wanted: bool = False,
    write: bool = False,
    file_path_to_send: str = ".",
) -> None:
    """
    This function is used to detect motion in a video file or from a webcam.
    It uses the MOG2 background subtraction algorithm to detect motion in the
    region of interest (ROI) and then draws a rectangle around the detected
    motion. The user can select a region of interest using the mouse. The
    program will then display the video with the detected motion highlighted
    by a red rectangle. The program will continue to run until the user
    presses the 'q' key or closes the window. The program will then release
    the video capture and close the windows.


    Parameters:
    source: str - The source of the video. Can be a file path or 'webcam'.
    roi_wanted: bool - If True, the user wants to select an ROI. Default is False.
    write: bool - If True, the user wants to write the output to a video file. Default is False.
    file_path_to_send: str - The file path to save the output video. Default is root directory.

    Returns:
    out: cv2.VideoWriter - The output video object.
    """

    # Initialize out variable
    out = None

    vs, coordinates = roi_and_getting_object(source, roi_wanted=roi_wanted)

    # If the user wants to write the output to a video file
    if write:
        try:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(
                file_path_to_send + "output.mp4", fourcc, 20.0, (640, 480)
            )
        except Exception as e:
            print(f"Error: {e}")
            return

    # Create the background subtractor object
    fgbg = cv2.createBackgroundSubtractorMOG2()

    # Loop through the video frames
    while vs.isOpened():
        ret, frame = vs.read()
        if not ret:
            print("Could not read frame from video")
            break

        # Getting ROI ready
        roi = preparation.getting_roi_ready(frame, roi_wanted, coordinates)

        # Apply the background subtractor to the ROI
        fgmask = fgbg.apply(roi)

        # Find contours in the ROI
        thresh = 85
        contours = preparation.finding_contour(fgmask, thresh)

        # Find motion in the ROI
        min_area = 500

        preparation.contour(contours, min_area, roi=roi)

        # Write the frame to the output video file
        if write and out:
            out.write(frame)

        # Show the resulting frame
        cv2.imshow("Motion Detection", frame)

        # Break the loop on 'q' key press or if the window was closed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        try:
            # Try to get the window property
            cv2.getWindowProperty("Motion Detection", 0)
        except cv2.error:
            # If an error is caught, it means the window has been closed
            break

    # Release the video capture and close windows
    vs.release()
    if write and out:
        out.release()
    cv2.destroyAllWindows()
    print("Completed, for now")

    return out


def cli_main() -> motion_detection:
    """
    This function is used to parse the command line arguments and call the motion_detection function.
    The function will then return the motion detection script in the command line interface.

    Has one required argument: source
    Optional arguments: roi_wanted, write, file_path_to_send

    Returns:
    Motion Detection Script in CLI
    """
    parser = argparse.ArgumentParser(description="Motion Detection Script")
    parser.add_argument(
        "--source", required=True, type=str, help="Source of video: filepath or webcam"
    )
    parser.add_argument(
        "--roi_wanted", action="store_true", help="Flag to select region of interest"
    )
    parser.add_argument(
        "--write", action="store_true", help="Flag to write output to file"
    )
    parser.add_argument(
        "--file_path_to_send",
        type=str,
        default=None,
        help="File path to save the output video",
    )

    args = parser.parse_args()
    return motion_detection(
        source=args.source,
        roi_wanted=args.roi_wanted,
        write=args.write,
        file_path_to_send=args.file_path_to_send,
    )


def roi_and_getting_object(source: str, roi_wanted: bool = False) -> tuple:
    """
    This function is used to select a region of interest (ROI) and get the video object.
    If the user wants to select an ROI, the function will prompt the user to select an ROI using the mouse.
    The function will then return the video object and the coordinates of the ROI.

    Args:
    source: str - The source of the video.
    roi_wanted: bool - If True, the user wants to select an ROI. Default is False.

    Returns:
    vs: cv2.VideoCapture - The video object.
    coordinates: tuple - The coordinates of the ROI.
    """
    coordinates = ()

    if roi_wanted:
        print("Select a region of interest using mouse.")

        # Get coordinates of ROI
        coordinates = tuple(preparation.get_roi_coordinates(source))

        print("Region of interest selected.")

    # Get Video Object
    vs = preparation.reading_file(source)

    return vs, coordinates


if __name__ == "__main__":
    cli_main()
