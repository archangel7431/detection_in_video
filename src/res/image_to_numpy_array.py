import numpy as np
from PIL import Image

#load the image file
frame_path="./src/res/video_1/color/frame180.jpg"
frame=Image.open(frame_path)

#converting image into numpy array
frame_array=np.array(frame)

#display resulting NumPy array
print(frame_array)
print(frame_array.shape)