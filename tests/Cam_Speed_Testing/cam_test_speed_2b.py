#!/usr/bin/env python3

from picamera2 import Picamera2, Preview
import libcamera
import time

if __name__ == "__main__":
    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration()
    preview_config["transform"] = libcamera.Transform(vflip=1, hflip=1)
    picam2.configure(preview_config)
    picam2.start()
    
    tot_pic = 100
    
    pic = 0
    start_time = time.time()
    while pic < tot_pic:
        name = "test"+".jpg"
        picam2.capture_file(name)
        pic = pic + 1
        print(pic)
    end_time = time.time()
    
    elapsed_time = end_time-start_time
    avg_time = elapsed_time/tot_pic
    
    print("elapsed time is ",elapsed_time," s.")
    print("avg time is ",avg_time," s.")
    print("frame rate is", 1/avg_time, "Hz.")



