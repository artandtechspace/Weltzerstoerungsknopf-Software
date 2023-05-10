from peripherals.PeripheralConfig import Outputs, Inputs
from loggingsystem.Logger import Logger
import RPi.GPIO as GPIO
import asyncio as aio
from utils.GPIOUtil import is_pressed, setup_as_inputs


class HandDevice:
    logger = Logger("HandDevice")

    def __init__(self):
        # Setups the gpio-pins
        # Outputs
        GPIO.setup([
            Outputs.Hand.GPIO_IN,
            Outputs.Hand.GPIO_OUT,
            Outputs.Hand.GPIO_ENABLED
        ], GPIO.OUT, initial=GPIO.LOW)
        # Inputs
        setup_as_inputs([
            Inputs.Hand.GPIO_HAND_END_SWITCH,
            Inputs.Buttons.GPIO_PRIME_SWITCH
        ])

    # Stops any hand movement
    def stop(self):
        self.logger.debug("stop", "Stopping all movements")
        try:
            GPIO.output(Outputs.Hand.GPIO_IN, 0)
            GPIO.output(Outputs.Hand.GPIO_OUT, 0)
            GPIO.output(Outputs.Hand.GPIO_ENABLED, 0)
        except Exception as e:
            self.logger.error_with_exception("stop", "Error while stopping!", e)

    # Opens the hand and blocks until that move is completed
    async def move_outside(self):
        self.logger.info("move_outside", "Hand moves outside")

        try:
            # Write to the outputs that the hand should go out
            GPIO.output(Outputs.Hand.GPIO_ENABLED, 1)
            GPIO.output(Outputs.Hand.GPIO_OUT, 1)
            GPIO.output(Outputs.Hand.GPIO_IN, 0)

            # Waits until the end-switch, which here is also the prime-button,
            # has been pressed
            while is_pressed(Inputs.Buttons.GPIO_PRIME_SWITCH):
                await aio.sleep(0.0001)

            self.logger.debug("move_outside", "Reached end, stopping")

            # Ends hand movement
            self.stop()
        except Exception as e:
            self.logger.error_with_exception("move_inside", "Exception while moving, stopping", e)
            # Unlikely to raise an error but in case it does the movement should
            # stop to prevent damage
            self.stop()

    # Moves the hand back inside and blocks until that move is completed
    async def move_inside(self):
        self.logger.info("move_inside", "Hand moves inside")
        try:
            # Write to the outputs that the hand should go in
            GPIO.output(Outputs.Hand.GPIO_ENABLED, 1)
            GPIO.output(Outputs.Hand.GPIO_IN, 1)
            GPIO.output(Outputs.Hand.GPIO_OUT, 0)

            # Waits until the end-switch for closing has been pressed
            while not is_pressed(Inputs.Hand.GPIO_HAND_END_SWITCH):
                await aio.sleep(0.0001)

            self.logger.debug("move_inside", "Reached end, stopping")

            # Ends hand movement
            self.stop()
        except Exception as e:
            self.logger.error_with_exception("move_inside", "Exception while moving, stopping", e)
            # Unlikely to raise an error but in case it does the movement should
            # stop to prevent damage
            self.stop()
