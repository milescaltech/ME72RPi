#!/usr/bin/env python3

from picamera2 import Picamera2, Preview
import libcamera
import cv2
from matplotlib import pyplot as plt

if __name__ == "__main__":
    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration()
    preview_config["transform"] = libcamera.Transform(vflip=1, hflip=1)
    picam2.configure(preview_config)
    picam2.start()
    
    while True:
        picam2.capture_file("cur_im.jpg")
        
        img = cv2.imread("cur_im.jpg")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        plt.subplot(1,1,1)
        plt.imshow(img_rgb)
        plt.show(block=False)
        plt.pause(3)
        plt.close()
        plt.pause(1)

