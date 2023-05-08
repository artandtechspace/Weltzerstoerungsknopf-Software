from peripherals.HandDevice import HandDevice
from peripherals.SmokeDevice import SmokeDevice
from peripherals.PrinterDevice import PrinterDevice
from peripherals.ScissorsDevice import ScissorsDevice
from animations.AnimationSystem import AnimationSystem
from config.ConfigSystem import ConfigSystem

# Data-class with instances of all core elements
class CoreData:

    def __init__(self):
        self.hand = HandDevice()
        self.scissors = ScissorsDevice()
        self.printer = PrinterDevice()
        self.smoker = SmokeDevice()
        self.animations = AnimationSystem()
        self.config = ConfigSystem()

    def initialize(self):
        self.config.initialize()