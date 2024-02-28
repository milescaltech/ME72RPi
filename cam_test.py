#!/usr/bin/env python3

import robot
import camera
import cv2
import numpy as np

if __name__ == "__main__":
    # Create the robot
    bob = robot.Robot()

    # Name of the JPEG image
    im_name = 'mynameiskyle'

    while True:
        try:
            bob.camera.capture(im_name)
            (img_rgb, img_grey, img_hsv) = camera.convert_img(im_name)
            circles = camera.find_circ(im_name)
            print(circles)

            if circles is not None:
                circles = np.uint16(np.around(circles))
        
                # Select the first circle as most prominent
                best_circle = circles[0][0]  # [x,y,r]
  
                # Add this hooligan to the frame
                cv2.circle(img_rgb, (best_circle[0], best_circle[1]), \
                           best_circle[2], (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Blob Detection", img_rgb)
           
            # Break the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise BaseException


        except BaseException as e:
            cv2.destroyAllWindows()
            bob.shutdown()
            print("Program terminated.")
            break
