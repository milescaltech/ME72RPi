#!/usr/bin/env python3

import serial
from time import sleep

ser = serial.Serial("/dev/ttyS0",115200)

while True:
    received_data = ser.read()  # read serial port
    sleep(0.03)
    data_left = ser.inWaiting()  # check for remaining byte
    received_data += ser.read(data_left)
    print(len(received_data))
