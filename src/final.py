import preparation
from roi_coordinates import coordinates_and_dimensions

print("Select a region of interest using mouse.")

# Get coordinates of ROI
roi_x, roi_y, roi_width, roi_height = coordinates_and_dimensions()

print("Region of interest selected.")

# Get VideoObject
args = preparation.argument_parser()
vs = preparation.reading_file(args=args)

# Initialize pygame
preparation.init_pygame()