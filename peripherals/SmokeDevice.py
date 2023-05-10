from peripherals.PeripheralConfig import Outputs
from loggingsystem.Logger import Logger
import asyncio as aio
from RPi import GPIO

class SmokeDevice:

    logger = Logger("SmokeDevice")

    def __init__(self):
        # Setups the gpio-pins
        # Outputs
        GPIO.setup([
            Outputs.SmokeDevice.GPIO_SMOKE_MACHINE_ENABLE,
        ], GPIO.OUT, initial=GPIO.LOW)

    # Enables the smoke device
    def enable(self):
        GPIO.output(Outputs.SmokeDevice.GPIO_SMOKE_MACHINE_ENABLE, 1)

    # Disables the smoke device
    def disable(self):
        GPIO.output(Outputs.SmokeDevice.GPIO_SMOKE_MACHINE_ENABLE, 0)

    # Run the smoker for a given time in seconds
    async def run_for(self, time: int):
        self.enable()
        await aio.sleep(time)
        self.disable()