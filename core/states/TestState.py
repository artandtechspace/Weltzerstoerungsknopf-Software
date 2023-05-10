import neopixel
from peripherals.tests.PeripheralTestTypes import PeripheralTestType
from core.CoreData import CoreData
from loggingsystem.Logger import Logger

logger = Logger("TestState")


async def turnoff_leds(pxls: neopixel.NeoPixel):
    pxls.fill((0, 0, 0))


async def start_test_state(core: CoreData, test: PeripheralTestType):
    # Disables all leds
    await core.animations.start_animation(turnoff_leds)
    # Plays the test
    await test.value[1](logger, core)
