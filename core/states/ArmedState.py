import neopixel
from peripherals.PeripheralConfig import Inputs
import asyncio as aio
from core.CoreData import CoreData
from utils.ButtonListeners import ButtonListener

async def __on_armed_animation(pxls: neopixel.NeoPixel):
    while True:
        await aio.sleep(1)
        pxls.fill((70,1,1))
        pxls.show()
        await aio.sleep(0.8)
        pxls.fill((0,0,0))
        pxls.show()
        await aio.sleep(0.8)

async def start_armed_state(core: CoreData):
    # Plays the default animation
    await core.animations.start_animation(__on_armed_animation)

    # Waits for one of the buttons to change
    state = await ButtonListener()\
        .wait_for_change(pin=Inputs.Buttons.GPIO_PRIME_SWITCH, to=False)\
        .wait_for_change(pin=Inputs.Buttons.GPIO_FIRE_BUTTON,  to=True)\
        .then()

    # Returns back to the idle-state if the prime-switch
    # got defused again
    if state == Inputs.Buttons.GPIO_PRIME_SWITCH:
        from core.states.IdleState import start_idle_state
        return start_idle_state

    # Else the fire-button got pressed and thus the fire-state starts
    from core.states.FireState import start_fire_state
    return start_fire_state
