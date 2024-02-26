#!/usr/bin/env python3

import os
import time

tot_pic = 10

if __name__ == "__main__":
    pic = 0
    start_time = time.time()
    while pic < tot_pic:
        os.system("libcamera-still -o test1.jpg -t 5 --vflip --hflip")
        pic = pic + 1
        print(f'photo no. {pic}')
    end_time = time.time()
    
    elapsed_time = end_time - -start_time
    avg_time = elapsed_time/tot_pic
    
    print("elapsed time is ",elapsed_time," s.")
    print("avg time is ",avg_time," s.")



