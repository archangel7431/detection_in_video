# Plan for completing the project-Image Processing(only for Riya and Joji- to be deleted after the project is done)


# Resources
## Folder structure for the project
https://github.com/yngvem/python-project-structure#the-setup-files

## Git tutorial from w3schools.com
https://www.w3schools.com/git/default.asp
(Use this for doubts about git or github)

## Installing *pyenv*
https://realpython.com/python-coding-setup-windows/
(refer the part related to *pyenv*)

### Virtual environment-*pyenv*
https://rkadezone.wordpress.com/2020/09/14/pyenv-win-virtualenv-windows/
### Comments:
*Create a global **python 3.11.3** environment*

## Windows 11 hotkeys
https://support.microsoft.com/en-us/windows/keyboard-shortcuts-in-windows-dcc61a57-8ff0-cffe-9796-cb9706c75eec

## Image *basics*
## Creating a Frame
https://www.simplilearn.com/image-processing-article

###***MUST READ THIS***
https://www.futurelearn.com/info/courses/introduction-to-image-analysis-for-plant-phenotyping/0/steps/305359

## 1. Setup the environment(Joji)

### 1.1 Clone repository
Copy the link of the repository and in the terminal, type:
``` git clone <URL> ```

### 1.2 Create a virtual environment(*env*)
```
PC> pyenv versions
PC> python -m pip install -user virtualenv
PC> python -m venv env
```

### 1.3 Activate *env* environemnt(do this everytime we start to work on the project)
```PC> .\env\Scripts\activate ```

### 1.4 Deactivate *env* environment(do this everytime you shut down the computer)
``` PC> deactivate ```

### 1.5 Install the dependencies 
Run `pip install -r requirements.txt` in the root directory of the project

### ***Comments***:
I have uploaded the video CLifford sir sent us onto the *res* directory.

You should create a git branch named *image_to_numpy_array*

For the file path in the converting to numpy file, use `path = ./res/video_1.mp4` in the python file.


## 2. Convert image to numpy array(Riya) - ***Image acquistion***
