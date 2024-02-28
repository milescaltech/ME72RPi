'''
Class for storing parameters and algorithms of the robot controller.

'''


class Controller:
    def __init__(self, nx, ny, num_channels=10):
        '''
        Parameters
        ----------
        nx: camera number of pixels in the x-direction
        ny: camera number of pixels in the y-direction
        num_channels: number of channels to compute values for
        '''

        # Controller constant parameters
        # Forward speed for ball capture
        self.K1 = 1.0

        # Yaw rate
        self.K2 = 1.0

        # Ascent/descent rate
        self.K3 = 1.0

        # Store the camera resolution
        self.nx = nx
        self.ny = ny

        # Channel values
        self.num_channels = num_channels
        self.ch = []
        for _ in range(self.num_channels+1):
            self.ch.append(0)

        self.mode = 'search'

    def compute_ch(self,DH,DV):
        '''
        Computes R/C transmitter channel values that would be entered to
        perform the desired maneuver.
        '''
        if self.get_mode() == 'seek':
            # First element is set to 1 to conform with iBus channel format
            self.ch[0] = 1
    
            # Right stick, left/right [-K1, +K1]
            self.ch[1] = self.K1*DH/(self.nx/2)
    
            # Right stick, forward/backward = K2
            self.ch[2] = self.K2
    
            # Left stick, forward/backward [0 K3]
            self.ch[3] = self.K3*abs(DV)/(self.ny/2)
    
            # Left stick, left/right (doesn't matter; no zero turn radius for ball
            # capture mode)
            self.ch[4] = 0
    
            # VRM dials
            # UPDATE WITH BALL BLOWER >> KAL
            self.ch[5] = 0
            self.ch[6] = 0
    
            # Far left switch
            if DV > 0:
                # Ball is below the center of frame; need to descend
                self.ch[7] = 1
            else:
                # Ball is above the center of frame; need to ascend
                self.ch[7] = 0
    
            # Middle left switch
            self.ch[8] = 0  # Do not use the zero-turn radius mode
    
            # Middle right switch
            self.ch[9] = 0
    
            # Far right switch
            self.ch[10] = 1  # Need to be in flight mode

        elif self.get_mode() == 'search':
            # UPDATE >> KAL
            for i in range(self.num_channels):
                self.ch[i] = 0
            self.ch[10] = 1

        return self.ch

    def set_mode(self, mode):
        '''
        Setter method for the current autonomy mode.

        Mode types:
        (1) search - did not find any balls, so go search for one
        (2) seek - found a ball, so go capture it
        (3) destroy - ball captured, so go score that mf
        '''
        self.mode = mode

    def get_mode(self):
        '''
        Getter method for the current autonomy mode.

        '''
        return self.mode


