
import neopixel
from core.CoreData import CoreData
import asyncio as aio

async def __on_reset_animation(pxl: neopixel.NeoPixel):
    pxl.fill((0,0,0))
    pxl.show()

async def start_reset_state(core: CoreData):
    # Stops any animations
    await core.animations.start_animation(__on_reset_animation)

    # Stops the smoke
    core.smoker.disable()

    # Performs the below tasks simultaneously
    await aio.gather(
        # Moves the hand inside
        core.hand.move_inside(),
        # Moves the scissors into it's start position
        core.scissors.open()
    )

    # Forwards to the starting idle state
    from core.states.IdleState import start_idle_state
    return start_idle_state
