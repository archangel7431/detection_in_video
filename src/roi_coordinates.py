# Import the required libraries
import cv2
import numpy as np
from roi_array import roi_array

# Finding roi coordinates
def roi_coordinates(roi, threshold1, threshold2):
    # Perform Canny edge detection
    edges = cv2.Canny(roi, threshold1, threshold2)

    # Find the coordinates of the edges
    edge_coordinates = np.nonzero(edges)
    edge_points = list(zip(edge_coordinates[1], edge_coordinates[0]))

    # Display the edge image
    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return edge_points


if __name__ == "__main__":
    roi = roi_array("./src/res/video_1/gaussian_blur/frame180.jpg")
    edge_points = roi_coordinates(roi, 0.0, 20)
    print(edge_points)