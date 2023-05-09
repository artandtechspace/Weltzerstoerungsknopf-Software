import neopixel
from peripherals.PeripheralConfig import Outputs, Inputs
import asyncio as aio
from core.CoreData import CoreData
from utils.ButtonListeners import ButtonListener

# Animation for the idle-state
async def __on_idle_animation(pxls: neopixel.NeoPixel):

    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    def wheel(pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return r, g, b

    # Creates a rainbow-cycle
    async def rainbow_cycle(wait_time):
        # Gets how many leds are defined
        led_amount = Outputs.Leds.LED_AMOUNT

        for j in range(255):
            for i in range(led_amount):
                pixel_index = (i * 256 // led_amount) + j
                pxls[i] = wheel(pixel_index & 255)
            pxls.show()
            await aio.sleep(wait_time)

    # Only plays the rainbow cycle while in idle state
    while True:
        await rainbow_cycle(0.01)

async def start_idle_state(core: CoreData):

    try:
        # Plays the default animation
        await core.animations.start_animation(__on_idle_animation)

        # Registers the button listener to
        # wait for the armed button
        await ButtonListener() \
            .wait_for_change(pin=Inputs.Buttons.GPIO_PRIME_SWITCH,to=True) \
            .then()

        # Forwards to the armed state
        from core.states.ArmedState import start_armed_state
        return start_armed_state
    except aio.CancelledError as e:
        pass
