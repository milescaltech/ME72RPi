#!/usr/bin/env python3

import time
from ibus import IBus

if __name__ == "__main__":
    # Create the iBus
    ibus_in = IBus()
    while True:
        # Read the channels; pray for success
        res = ibus_in.read()
        print('Status {} CH1 {} CH2 {} CH3 {} CH4 {} CH5 {} CH6 {}'.format(
              res[0],res[1],res[2],res[3],res[4],res[5],res[6]), end=" ")
        print('CH7 {} CH8 {} CH9 {} CH10 {}'.format(res[7],res[8],res[9],res[10]))
