import neopixel
import asyncio as aio
from core.CoreData import CoreData
from peripherals.PeripheralConfig import Outputs
import Config

async def __on_scissors_animation(pxls: neopixel.NeoPixel):
    # Animates a small countdown

    pxls.fill((255, 0, 0))
    pxls.show()
    for i in range(Outputs.Leds.LED_AMOUNT - 1, 0, -1):
        pxls[i] = (0, 0, 0)
        pxls.show()
        await aio.sleep(0.4)
    pxls.fill((0, 255, 0))
    pxls.show()


async def __on_fire_animation(pxls: neopixel.NeoPixel):
    while True:
        pxls.fill((0, 0, 0))
        pxls.show()
        await aio.sleep(0.5)
        pxls.fill((255, 0, 0))
        pxls.show()
        await aio.sleep(0.5)


'''
Returns the constructed text to print and increments the counter
'''


def __get_print_text():
    # Builds the text
    return Config.TEXT.replace("%counter%", str(Config.COUNTER))


'''
Returns the filename of the image for the current counter
'''


# TODO: Implement images
def __get_print_image():
    # Special secret number to print franz amtmann
    SPECIAL_NUMBERS = [42, 1337, 69, 333, 314, 271, 161, 911]

    # Checks for the special numbers
    if Config.COUNTER in SPECIAL_NUMBERS:
        return "amtmann.png"

    # Checks for a very special number
    if Config.COUNTER == 420:
        return "hanf.png"

    # Default no special return
    return "explosion.png"


async def start_fire_state(core: CoreData):
    # Plays the fire animation
    await core.animations.start_animation(__on_fire_animation)

    # Runs the smoker for a second
    tsmoker = core.smoker.run_for(1)

    # Moves the hand out and in again
    await core.hand.move_outside()
    await core.hand.move_inside()

    # Ensures the smoker has finished his operation
    await tsmoker

    # Increments the counter
    Config.COUNTER += 1

    # Prints the info-data
    core.printer.print_preset(text=__get_print_text(), image=__get_print_image())

    # Waits a short time
    await aio.sleep(0.5)

    # Starts the scissors animation
    await core.animations.start_animation(__on_scissors_animation)

    # Starts the scissors
    await core.scissors.close()
    await core.scissors.open()

    # Continues to the idle state
    from core.states.IdleState import start_idle_state
    return start_idle_state
