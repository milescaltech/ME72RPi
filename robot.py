'''
Parent class for our thicc bot.

'''

# System shit
import pigpio
import sys

# Homemade
import motor
from ibus import IBus

# Define motor pins
PN_ESCL = 26
PN_ESCR = 19
PN_ESCV = 16

# Define speed reduction parameters
alpha_LR = 0.7
alpha_V = 0.5

# Define how much max values can be exceed before terminating the program
margin = 0.02

# Toggle cubic mixing
cubic_mix = False


class Robot:
    def __init__(self):
        print("Setting up GPIO...")
        
        # Create an IO interface
        self.io = pigpio.pi()

        if not self.io.connected:
            # Make sure the shits connected
            print("Unable to connect to pigpio daemon!")
            sys.exit(0)

        # Connect the iBus
        print("Setting up the iBus...")
        self.ibus = IBus()

        # Create left EDF
        self.left_motor = motor.Motor(self.io, PN_ESCL)

        # Create right EDF
        self.right_motor = motor.Motor(self.io, PN_ESCR)

        # Create vertical EDF
        self.vertical_motor = motor.Motor(self.io, PN_ESCV)

        # Successful connection to daemon and attachment of output pins
        print("GPIO ready!")

        # Initialize robot attributes
        # --altitude
        # --gyro stuff
        # --what else...

        # Add stop falgs and SO FORTH

    def get_io(self):
        '''
        Getter method for the IO interface.
        '''
        return self.io

    def read_channels(self):
        '''
        Read channel values using the iBus serial communication protocol.
        '''
        self.ibus.read()
        return self.ibus.get_ch()

    def set_motors(self):
        '''
        Sets motor values based on channel values.
        '''
        # Get channel values from the iBus
        ch = self.ibus.get_ch()

        # Convert values to power in [-1.0, +1.0]
        for i in range(len(ch)):
            if i in [1,2,4]:
                # Continuous [-1, 1]
                ch[i] = motor.map_value(ch[i],1000,2000,-1,1)
            elif i in [3,5,6]:
                # Continuous [0, 1]
                ch[i] = motor.map_value(ch[i],1000,2000,0,1)
            elif i in [7,8,10]:
                # Discrete {0, 1}
                ch[i] = round(motor.map_value(ch[i],1000,2000,0,1))
            elif i == 9:
                # Discrete {0, 1, 2}
                ch[i] = round(motor.map_value(ch[i],1000,2000,0,2))

        # Flight switch up; turn off all motors
        if ch[10] == 0:
            lspeed = 0
            rspeed = 0
            vspeed = 0
        # Otherwise, fly normally
        else:
            # Normal linear channel mixing
            lspeed = 0.5*alpha_LR*(ch[2] + ch[1])
            rspeed = 0.5*alpha_LR*(ch[2] - ch[1])

            if cubic_mix:
                # Apply cubic mixing (might want to implement 3/2 mixing)
                lspeed = 0.5*alpha_LR*(ch[2] + ch[1]**3)
                rspeed = 0.5*alpha_LR*(ch[2] - ch[1]**3)
            
            if ch[8] == 1:
                # Zero turn radius mode
                lspeed = alpha_LR*ch[4]
                rspeed = -alpha_LR*ch[4]

            # Vertical motor
            vspeed = alpha_V*ch[3]
            if ch[7] == 1:
                # Reverse motor direction to go down
                vspeed = -vspeed
       
        # Write powers to the motors
        self.left_motor.set_speed(lspeed)
        self.right_motor.set_speed(rspeed)
        self.vertical_motor.set_speed(vspeed)

    def get_motor(self, mtype):
        '''
        Getter method for motor `mtype`.
        Left ('L'), right ('R'), vertical ('V')
        '''
        if mtype == 'L':
            return self.left_motor
        elif mtype == 'R':
            return self.right_motor
        elif mtype == 'V':
            return self.vertical_motor
        else:
            # Not a valid motor
            return None

    def shutdown(self):
        '''
        Clears motor pins and closes the IO interface.
        '''
        print("Turning off...")

        # Clear motor shit
        self.left_motor.stop()
        self.right_motor.stop()
        self.vertical_motor.stop()

        # Stop the IO interface
        self.io.stop()

    
