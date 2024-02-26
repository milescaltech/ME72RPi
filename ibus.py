'''
Used to interface with the FlySky FS-iA10B receiver.
'''


import serial


class IBus:
    def __init__ (self, baud=115200, num_channels=10, nbytes=32):
        # Baud rate
        self.baud = baud

        # UART pin on Raspberry Pi 4 Model B
        self.uart = serial.Serial("/dev/ttyS0", baud)

        # Number of receiver channels
        self.num_channels = num_channels

        # Number of bytes transmitted by iBus in each message
        self.nbytes = nbytes

        # Channel values
        self.ch = []

        # Initialize channel values to 0
        for _ in range (self.num_channels + 1):
            self.ch.append(0)
            
    def read(self):
        '''
        Read the channel values using iBus serial communication protocol.
        
        Returns list of channel values. First value is status:
        1 = new values
        0 = checksum error
        -1 = other error; return previous channel values

        Remaining ten values are for CH1 - CH10.

        Little endian byte order!
        '''

        # Read until you get the header
        while True:
            char = self.uart.read(1)
            if char == b'\x20':
                break

        # Read the remaining bytes into a buffer
        buffer = self.uart.read(self.nbytes-1)

        # Check the second byte is correct
        if buffer[0] != 0x40:
            print('CRITICAL ERROR: second byte in iBus stream incorrect')
            # Set status to failure and do not change channel values
            self.ch[0] = -1
            return self.ch

        # Compute checksum - subtract byte values from 0xffff for bytes 1-30
        checksum = 0xffff - 0x20
        for i in range(self.nbytes-3):  # DO NOT INCLUDE CHECKSUM VALUES
            checksum -= buffer[i]

        # Termiante if checksum does not match
        if checksum != (buffer[-2] + (buffer[-1] << 8)):
            print('CHECKSUM ERROR: checksum does not match end bytes')
            # Set status to checksum failure and do not change channel values
            self.ch[0] = 0
            return self.ch

        self.ch[0] = 1 # status 1 = success
        # Read in the channels
        for i in range (1, self.num_channels + 1):
            self.ch[i] = (buffer[(i*2)-1] + (buffer[i*2] << 8))    
        return self.ch

    def get_ch(self):
        '''
        Getter method for channel values.
        '''
        return self.ch
