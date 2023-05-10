'''
Input peripherials
'''

# Used for inverted inputs
INVERTED = True
NOT_INVERTED = False


class InternalInputs_Scissors:
    # GPIO-Pins for the end-switches for the scissors on a position
    GPIO_OPEN = (19, NOT_INVERTED)
    GPIO_CLOSE = (6, NOT_INVERTED)


class InternalInputs_Buttons:
    # GPIO-pins for the user buttons
    # Main fire-button to start the destruction
    GPIO_FIRE_BUTTON = (17, INVERTED)
    # Prime switch to prepare the main switch
    GPIO_PRIME_SWITCH = (5, INVERTED)


class InternalInputs_Hand:
    # GPIO-Pin for the end-switch of the hand (Inside end switch, outside is the normal prime-button)
    GPIO_HAND_END_SWITCH = (27, INVERTED)


# General input-pin definitions
class Inputs:
    Scissors = InternalInputs_Scissors
    Buttons = InternalInputs_Buttons
    Hand = InternalInputs_Hand


'''
Output peripherials
'''


# Output pin definitions for the scissors
class InternalOutputs_Scissors:
    # To move the scissors up or down, the specific
    # GPIO pin must be set to 1 and its counterpart
    # to 0
    GPIO_CLOSE = 26
    GPIO_OPEN = 13


# Output pin definitions for the hand
class InternalOutputs_Hand:
    # To move the hand out or in, the specific
    # GPIO pin must be set to 1 and its counterpart
    # to 0, also the ENABLE_PIN must also be high
    GPIO_OUT = 9
    GPIO_IN = 10
    GPIO_ENABLED = 11


# Output pin definitions for the smoke device
class InternalOutputs_SmokeDevice:
    # To enable the smoke device, enable this pin
    GPIO_SMOKE_MACHINE_ENABLE = 16


# Output settings for the printer
class InternalOutputs_Printer:
    # USB-Ids for the printer
    VENDOR_ID = 0x0416
    PRODUCT_ID = 0x5011


# Output settings for the leds
class InternalOutputs_LEDS:
    # How many leds are connect
    LED_AMOUNT = 29

    # Further neopixel settings like RGB/GRB-Order or the bord-pin must directly be done inside the
    # animation-system file


# General output-pin definitions
class Outputs:
    Scissors = InternalOutputs_Scissors
    Hand = InternalOutputs_Hand
    SmokeDevice = InternalOutputs_SmokeDevice
    Printer = InternalOutputs_Printer
    Leds = InternalOutputs_LEDS
