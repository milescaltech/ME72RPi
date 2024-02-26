#!/usr/bin/env python3

from picamera2 import Picamera2
import time

tot_pic = 100


if __name__ == "__main__":
    camera = Picamera2()
    camera.start()
    
    pic = 0
    start_time = time.time()
    while pic < tot_pic:
        camera.capture_file("test.jpg")
        pic = pic + 1
        print(pic)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    avg_time = elapsed_time/tot_pic
    
    print("elapsed time is ",elapsed_time," s.")
    print("avg time is ",avg_time," s.")
    print("frame rate is", 1/avg_time, "Hz.")



