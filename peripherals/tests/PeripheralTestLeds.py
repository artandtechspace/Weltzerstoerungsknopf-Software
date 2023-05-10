from core.CoreData import CoreData
import asyncio as aio
from loggingsystem.Logger import Logger
import neopixel


async def on_test_animation(pxls: neopixel.NeoPixel):
    # Plays R-G-B-W for all pixels
    pxls.fill((255, 0, 0))
    pxls.show()
    await aio.sleep(1)
    pxls.fill((0, 255, 0))
    pxls.show()
    await aio.sleep(1)
    pxls.fill((0, 0, 255))
    pxls.show()
    await aio.sleep(1)
    pxls.fill((255, 255, 255))
    pxls.show()
    await aio.sleep(1)
    pxls.fill((0, 0, 0))
    pxls.show()


# Tests the leds
async def on_leds_test(logger: Logger, core: CoreData):
    logger.debug("on_leds_test", "=== starting test")
    # Starts the animation and waits for it's finishing
    await core.animations.start_animation(on_test_animation)
    await aio.sleep(4.5)
    logger.debug("on_leds_test", "=== ending test")
