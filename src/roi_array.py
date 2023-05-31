# Importing necessary libraries
import cv2

# Function to handle mouse events
def select_roi(event, x, y, flag, param):
    global roi_pts, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_pts = [(x, y)]
        roi_selected = False

    elif event == cv2.EVENT_LBUTTONUP:
        roi_pts.append((x,y))
        roi_selected = True

        # Draw the selected ROI rectangle
        cv2.rectangle(image, roi_pts[0], roi_pts[1], (0, 255, 0), 2)
        cv2.imshow("Select ROI", image)
    

def roi_array(path):
    # Read the image
    global image, roi_selected,roi_pts
    image = cv2.imread(path)

    # Creating a window to display the image
    cv2.namedWindow("Image")
    cv2.imshow("Image", image)

    # Initialize ROI variables
    roi_pts = []
    roi_selected = False

    # Call the function to handle mouse events
    cv2.setMouseCallback("Image", select_roi)

    # Selecting roi using mouse
    while not roi_selected:
        cv2.imshow("Image", image)
        cv2.waitKey(1)

    # Extracting ROI into numpy array
    # roi = image[roi_pts[0][1]:roi_pts[1][1], roi_pts[0][0]:roi_pts[1][0]]

    return roi_pts


if __name__ == "__main__":
    roi = roi_array(path="./src/res/video_1/gaussian_blur/frame60.jpg")
    print(roi)