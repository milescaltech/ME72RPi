#!/usr/bin/env python3

import robot
from motor import map_value
import time

if __name__ == "__main__":
    # Create robot
    robot = robot.Robot()
    print("Robot ready!")

    print("Let the ESCs turn on. Standing by...")
    time.sleep(3)

    while True:
        try:
            # Read the channel values
            robot.read_channels()

            # Set the motor powers based on current channel values
            robot.set_motors()
            print(f'LEFT {robot.left_motor.get_speed():.2f} | RIGHT '
                  f'{robot.right_motor.get_speed():.2f} | VERT '
                  f'{robot.vertical_motor.get_speed():.2f}')


        except BaseException as e:
            # Keyboard interrupt used to stop the program and shutdown robot
            print(e)
            robot.shutdown()
            break
