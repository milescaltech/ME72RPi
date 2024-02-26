'''
Controls robot motors (ESCs)

'''

import pigpio

# Arbitrary maximum value for motor speed values
MAX_VAL = 100

# Helper functions
def map_value(x, x1, x2, y1, y2):
    '''
    Creates a linear mapping between (x1, y1) --> (x2, y2) and computes the
    associated y-value corresponding to the provided x-value.

    Exactly the same behavior as the Arduino map function.
    '''
    val = y1 + (y2 - y1)/(x2 - x1)*(x - x1)
    return val


class Motor:
    def __init__(self, io_object, pin_no):
        # IO interface created in robot class
        self.io = io_object

        # Set pin number
        self.pin_no = pin_no

        # Set pin as output
        self.io.set_mode(pin_no, pigpio.OUTPUT)

        # Start with motor off
        self.io.set_servo_pulsewidth(pin_no, 0)

        # Store motor speed
        self.speed = 0

    def set_speed(self, power):
        '''
        Sets the appropraite pulse width (in microseconds) on the given motor
        based on the requsted speed, which takes values in [-1.0, +1.0]
        
        Negative values put the motor in reverse; positive values forward.
        '''
        # Check the speed is in the allowable range
        if abs(power) > 1:
            raise BaseException("Speed out of range!")

        # Store the speed attribute
        self.speed = power*MAX_VAL

        # Convert the speed value to a pulse width
        pw_usec = map_value(self.speed, -MAX_VAL, MAX_VAL, 1000, 2000)

        # Set the pulse width on the pin
        self.io.set_servo_pulsewidth(self.pin_no, pw_usec)
    
    def get_speed(self):
        '''
        Get the current speed value of the motor.
        '''
        # Obtain the pulse width directly from the IO object
        microseconds_val = self.io.get_servo_pulsewidth(self.pin_no)

        # Map the pulse width to a speed value
        return map_value(microseconds_val, 1000, 2000, -MAX_VAL, MAX_VAL)
    
    def get_pin_no(self):
        '''
        Get this motor's GPIO pin number.
        '''
        return self.pin_no

    def stop(self):
        '''
        Turns off the motor pin.
        '''
        self.io.set_servo_pulsewidth(self.pin_no, 0)
