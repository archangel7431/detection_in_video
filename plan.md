## Using motion detection
To use the function `motion_detection` in `.\src\final.py`, we have the following options:
1. In the `main funcion`, simply run `cli_main()`. This is the CLI interface. It has one required option and 4 optional options.

    Eg: a) `$python .\src\final.py --source webcam`

    This runs the motion_detection in webcam with no ROI or writing to a file.

    b) ``$python .\src\final.py --source webcam --roi_wanted``

    This runs the motion_detection for webcam with ROI but not writing to a file.

    NOTE:

    Don't try to use the `write` or `file_path_to_send` option, for now. It has not been tested.

2. In the `main` function, run:
```
source = "webcam"
motion_detection(source)
```
This will run motion_detection on the source, here 'webcam'. This can be done by simply running the file or running `python .\src\final.py` in the command line.

This should be able to handle files also. If wrong file is given, it will point out an error.

`roi_wanted = True` can be used to get ROI in the source.

Other parameters are not fully tested.

## Test the above functionalities




## Comments
The ROI drawn is dependent on the point in which it clicks. It calculates the distances and draws the rectangle to the right and downward.

Although I tried correcting it and has succeeded in correcting the direction, the box now gets bigger than I draw. Need to correct this.