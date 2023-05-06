from Logger import Logger
import asyncio as aio
import board
import neopixel
from peripherals.PeripheralConfig import Outputs

class AnimationSystem:

    logger = Logger("AnimationSystem")

    def __init__(self):

        # Neopixel-api to access leds
        self.__pixels = neopixel.NeoPixel(board.D21, Outputs.Leds.LED_AMOUNT, brightness=1, auto_write=False, pixel_order=neopixel.GRB)

        # Animation that currently is playing
        self.__currently_playing : aio.Task|None = None

    # Event: When a animation ends
    def __on_animation_end(self, _):
        self.__currently_playing = None

    # Stops the animation if it's playing
    async def kill_animation(self):

        # Ensures there is an animation playing
        if self.__currently_playing is None:
            return

        # Kills the animation
        try:
            self.__currently_playing.cancel()
            await self.__currently_playing
        except:
            pass
        self.__currently_playing = None

    '''
    Starts to play a new animation
    
    :param animation is a async function that plays the animation after the below definition:
    
    def animation_one(pixel_access: Neopixel) -> None
    '''
    async def start_animation(self, animation):

        # Ensures no other animation is playing
        await self.kill_animation()
        # Starts the new animation
        self.__currently_playing = aio.create_task(animation(self.__pixels))
        # Binds a reset-function
        self.__currently_playing.add_done_callback(self.__on_animation_end)
