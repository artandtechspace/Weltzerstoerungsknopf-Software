import RPi.GPIO as GPIO

'''
Takes in the new format of (pinid, is_inverted) and setups them as inputs
'''
def setup_as_inputs(pins: [(int, bool)]):
    GPIO.setup(
        list(map(lambda x: x[0], pins)),
        GPIO.IN
    )


'''
Returns if a given pin is pressed
:param pin is a tuple of (pinid, is_inverted)
'''


def is_pressed(pin: (int, bool)):
    '''
    Truth-Table for the expression below:
    state, inverted, returnvalue
    0      0         0
    0      1         1
    1      0         1
    1      1         0
    '''
    return GPIO.input(pin[0]) != pin[1]
