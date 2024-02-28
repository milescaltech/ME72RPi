#!/usr/bin/env python3

from circle_detection_test import take_pic, convert_pic, plot_img, find_circ, add_circ, eval_circ, hsv_mask
import numpy as np
import matplotlib.pyplot

lower_color = np.array([100, 100, 100])
upper_color = np.array([140,255,255])

if __name__ == "__main__":
    name = "cont_test"

    while True:
        take_pic(name)
        img_rgb, img_grey, img_hsv = convert_pic(name)
        mask = hsv_mask(img_hsv,lower_color,upper_color)
        #plot = plot_img(img_rgb)
        circles = find_circ(mask)
        #add_circ(img_rgb,circles)
        x,y,r = eval_circ(circles)
        if str(x).isnumeric() == True:
            print("x: "+str(x)+",y: "+str(y)+",r: "+str(r))
        #add_circ(img_rgb, circles)
        #plot_img(img_rgb)
        print("___________________________")
