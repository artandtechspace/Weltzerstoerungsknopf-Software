from peripherals.HandDevice import HandDevice
from peripherals.SmokeDevice import SmokeDevice
from peripherals.PrinterDevice import PrinterDevice
from peripherals.ScissorsDevice import ScissorsDevice
from animations.AnimationSystem import AnimationSystem
from config.ConfigSystem import ConfigSystem
from RPi import GPIO
from utils.GPIOUtil import setup_as_inputs
from peripherals.PeripheralConfig import Inputs

# Data-class with instances of all core elements
class CoreData:

    def __init__(self):
        # TODO: Move somewhere better
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.hand = HandDevice()
        self.scissors = ScissorsDevice()
        self.printer = PrinterDevice()
        self.smoker = SmokeDevice()
        self.animations = AnimationSystem()
        self.config = ConfigSystem()

        # Setups missing buttons
        setup_as_inputs([
            Inputs.Buttons.GPIO_PRIME_SWITCH,
            Inputs.Buttons.GPIO_FIRE_BUTTON
        ])

    def initialize(self):
        self.config.initialize()