from peripherals.PeripheralConfig import Outputs, Inputs
from loggingsystem.Logger import Logger
import RPi.GPIO as GPIO
import asyncio as aio


class ScissorsDevice:
    logger = Logger("ScissorsDevice")

    def __init__(self):
        # Setups the gpio-pins
        # Outputs
        GPIO.setup([
            Outputs.Scissors.GPIO_OPEN,
            Outputs.Scissors.GPIO_CLOSE
        ], GPIO.OUT, initial=GPIO.LOW)
        # Inputs
        GPIO.setup([
            Inputs.Scissors.GPIO_CLOSE,
            Inputs.Scissors.GPIO_OPEN
        ], GPIO.IN)


    # Stops any scissor movement
    def stop(self):
        try:
            GPIO.output(Outputs.Scissors.GPIO_OPEN, 0)
            GPIO.output(Outputs.Scissors.GPIO_CLOSE, 0)
        except:
            pass

    # Opens the scissors and blocks until that move is completed
    async def open(self):
        try:
            # Write to the outputs that the sissor should open
            GPIO.output(Outputs.Scissors.GPIO_OPEN, 1)
            GPIO.output(Outputs.Scissors.GPIO_CLOSE, 0)

            # Waits until the end-switch for opening has been pressed
            while not GPIO.input(Inputs.Scissors.GPIO_OPEN):
                await aio.sleep(0.0001)

            # Ends scissors movement
            self.stop()
        except:
            # Unlikely to raise an error but in case it does the movement should
            # stop to prevent damage
            self.stop()

    # Closes the scissors and blocks until that move is completed
    async def close(self):
        try:
            # Write to the outputs that the scissors should close
            GPIO.output(Outputs.Scissors.GPIO_CLOSE, 1)
            GPIO.output(Outputs.Scissors.GPIO_OPEN, 0)

            # Waits until the end-switch for closing has been pressed
            while not GPIO.input(Inputs.Scissors.GPIO_CLOSE):
                await aio.sleep(0.0001)

            # Ends scissor movement
            self.stop()
        except:
            # Unlikely to raise an error but in case it does the movement should
            # stop to prevent damage
            self.stop()
