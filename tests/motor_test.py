#!/usr/bin/env python3

import robot
import time

if __name__ == "__main__":
    # Create robot 
    robot = robot.Robot()
    print("Robot ready!")

    try:
        robot.left_motor.set_speed(0)
        time.sleep(3)
        for i in range(-100,100):
            pwr = 1.0*i/100
            robot.left_motor.set_speed(pwr)
            print(f'Pin No. {robot.left_motor.get_pin_no()} | Speed ' 
                            f'{robot.left_motor.get_speed()}')
            time.sleep(0.04)
            robot.left_motor.set_speed(0)
        print("Task successfully completed.")
        robot.shutdown()
    except BaseException as e:
        print(e)
        robot.shutdown()
