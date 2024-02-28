'''
Parent class for our thicc bot.

'''

# System shit
import pigpio
import sys

# Homemade
import motor
from ibus import IBus
import camera
import controller

# Define motor pins
# UPDATE BLOWER FAN >> KAL
PN_ESCL = 26
PN_ESCR = 19
PN_ESCV = 16

# Define speed reduction parameters
alpha_LR = 0.7
alpha_V = 0.5

# Define motor curve intercept adjustment parameter
alpha_Itcp = 0.7

# Define how much max values can be exceed before terminating the program
margin = 0.02

# Toggle cubic mixing
cubic_mix = False


class Robot:
    def __init__(self, photo_name='oh_baby'):
        '''
        Parameters
        ----------
        photo_name: string specifying the name of the JPEG MAFIA to save
            for all the camera stuff
        '''

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

        # Create the camera
        print("Attaching the camera to the robot...")
        self.camera = camera.Camera()

        # Create the photo name
        self.photo_name = photo_name

        # Create the controller
        self.controller = controller.Controller( \
                        self.camera.resolution[0], \
                        self.camera.resolution[1], \
                        num_channels=self.ibus.num_channels)
        
#         # Store the latest robot channel commands
#         self.ch = []
#         for _ in range(self.ibus.num_channels)

        # Create left EDF
        self.left_motor = motor.Motor(self.io, PN_ESCL)

        # Create right EDF
        self.right_motor = motor.Motor(self.io, PN_ESCR)

        # Create vertical EDF
        self.vertical_motor = motor.Motor(self.io, PN_ESCV)

        # Successful connection to daemon and attachment of output pins
        print("GPIO ready!")

        # Manual or autonomous?
        self.autonomous = True

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
        if self.autonomous:
            # Take a picture with the camera
            self.camera.capture(self.photo_name)

            # Detect the circles
            circles = camera.find_circ(self.photo_name)

            # Camera detected at least one ball
            if circles is not None:
                # Set the controller mode to capture the ball
                self.controller.set_mode('seek')

                # Choose the best ball
                best_circle = circles[0][0]
    
                # Compute the horizontal and vertical distances from the frame
                # center to the ball center
                DH = best_circle[0] - self.camera.resolution[0]/2
                DV = best_circle[1] - self.camera.resolution[1]/2
    
                # Construct channel values from camera data and PD controller
                ch = self.controller.compute_ch(DH,DV)
            else:
                # Set the controller mode to look for ballz
                self.controller.set_mode('search')

                # Compute channels to spin - DH and DV values do not matter
                ch = self.controller.compute_ch(0,0)
        else:
            # Get channel values from the iBus
            ch = self.ibus.get_ch()  # [1000, 2000] us
    
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

        # Translate channel values to motor speeds
        # Flight switch up; turn off all motors
        if ch[10] == 0:
            lspeed = 0
            rspeed = 0
            vspeed = 0
        # Otherwise, fly normally
        else:
            # Normal linear channel mixing
            lspeed = alpha_LR*(alpha_Itcp*ch[2] + (1 - alpha_Itcp)*ch[1])
            rspeed = alpha_LR*(alpha_Itcp*ch[2] - (1 - alpha_Itcp)*ch[1])

            if cubic_mix:
                # UPDATE >> KAL
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

#         # Remove the camera
#         self.camera.close()

        # Stop the IO interface
        self.io.stop()

    
