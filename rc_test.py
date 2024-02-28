#!/usr/bin/env python3

import robot
import camera
import cv2
from motor import map_value
import time
import numpy as np

if __name__ == "__main__":
    # Create robot
    robot = robot.Robot()
    print("Robot ready!")
    print("Let the ESCs turn on. Standing by...")
    time.sleep(3)

    while True:
        try:
            if not robot.autonomous:
                # Read the channel values for manual piloting
                robot.read_channels()

            # Set the motor powers based on current channel values
            robot.set_motors()
            print(f'LEFT {robot.left_motor.get_speed():.2f} | RIGHT '
                  f'{robot.right_motor.get_speed():.2f} | VERT '
                  f'{robot.vertical_motor.get_speed():.2f}')

            # The rest of this is for plotting the camera feed to visualize
            # what the hell is going on
            (img_rgb, img_grey, img_hsv) = camera.convert_img(robot.photo_name)
            circles = camera.find_circ(robot.photo_name)

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
            # Keyboard interrupt used to stop the program and shutdown robot
            print(e)
            cv2.destroyAllWindows()
            robot.shutdown()
            print("Program terminated.")
            break
