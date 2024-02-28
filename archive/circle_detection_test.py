from picamera2 import Picamera2, Preview
import libcamera
import cv2
from matplotlib import pyplot as plt
import numpy as np

# setup camera with correct items
print("Configuring camera...")
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()
preview_config["transform"] = libcamera.Transform(vflip=1, hflip=1)
picam2.configure(preview_config)
picam2.start()
print("Camera configured!!!")

#function to take picture
def take_pic(name):
    pic_name = name+".jpg"
    picam2.capture_file(pic_name)
    
#function to read picture and convert to gray and rgb images
def convert_pic(name):
    pic_name = name+".jpg"
    img = cv2.imread(pic_name)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return img_rgb, img_grey, img_hsv

#function to apply hsv mask
def hsv_mask(img_hsv, lower_color, upper_color):
    mask = cv2.inRange(img_hsv, lower_color, upper_color)
    return mask
    
#function to plot image
def plot_img(img_rgb):
    plt.subplot(1,1,1)
    plt.imshow(img_rgb)
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    plt.pause(1)

#function to find circles
def find_circ(img_grey):
    # Apply Gaussian blur to reduce noise and help with detection
    blurred = cv2.GaussianBlur(img_grey, (5,5), 0)
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1 = 50, param2=30, minRadius=10, maxRadius=80)
    return circles

#function to add circles to plot
def add_circ(img_rgb,circles):
    if circles is not None:
        circles = np.round(circles[0,:]).astype("int")
        
        for (x,y,r) in circles:
            cv2.circle(img_rgb, (x,y), r, (0,255,0), 4)
            cv2.rectangle(img_rgb, (x-5, y-5), (x+5, y+5), (0,128,255),-1)
    #else:
        #print("No circles detected :(")
            
#function to get x,y,r values for circles
def eval_circ(circles):
    if circles is not None:
        circles = np.round(circles[0,:]).astype("int")
        for (x,y,r) in circles:
            return x,y,r
    else:
        print("No circles detected!")
        x = "none"
        y = "none"
        r = "none"
        return x,y,r

