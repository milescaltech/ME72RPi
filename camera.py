'''
Class and functions for camera shit.

'''

from picamera2 import Picamera2
import libcamera
import cv2
import numpy as np


def convert_img(im_name):
    '''
    Converts a JPEG image file (exclude the .jpg extenion!) to the three
    formats (1) RGB, (2) GREY, (3) HSV.
    '''
    # Open the JPEGMAFIA
    img = cv2.imread(im_name + ".jpg")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return (img_rgb, img_grey, img_hsv)

def find_circ(im_name, lc=np.array([100,100,100]), uc=np.array([140,255,255])):
    '''
    Returns a list of detected circles using an OpenCV algorithm.

    Parameters
    ----------
    im_name: name of the JPEG image file, excluding the extension
    lc: lower colors for HSV thresholding
    uc: upper colors for HSV thresholding
    '''
    # Get the three image pixel formats for the provided JPEG
    (img_rgb, img_grey, img_hsv) = convert_img(im_name)

    # Apply HSV thresholding
    masked = cv2.inRange(img_hsv, lc, uc)

    # Apply Gaussian blur to reduce noise and help with detection
    blurred = cv2.GaussianBlur(masked, (5,5), 0)

    # Identify the detected circles using OpenCV
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1,
                               minDist=20, param1 = 50, param2=30,
                               minRadius=20, maxRadius=120)
    return circles


class Camera:
    def __init__(self):
        # Create the camera object
        print("Setting up your beautiful camera...")
        self.camera = Picamera2()
        print("Camera created!")

        # Camera resolution
        self.resolution = (640, 480)

        # Configure the camera (preview config)
        pc = self.camera.create_preview_configuration()
        pc["transform"] = libcamera.Transform(vflip=1, hflip=1)
        self.camera.configure(pc)
        self.camera.start()
        print("Camera configured!")

    def capture(self,im_name):
        '''
        Captures an image and saves it using the provided name to the local
        directory.
        '''
        # Capture JPEG (try to store this in an array instead for speed!)
        self.camera.capture_file(im_name + ".jpg")

    def get_camera(self):
        '''
        Getter method for the camera object.
        '''
        return self.camera


