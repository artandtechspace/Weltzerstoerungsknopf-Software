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
        self.logger.info("enable", "Starting smoker")
        try:
            GPIO.output(Outputs.SmokeDevice.GPIO_SMOKE_MACHINE_ENABLE, 1)
        except Exception as e:
            self.logger.error_with_exception("stop", "Error while stopping!", e)
            pass

    # Disables the smoke device
    def disable(self):
        self.logger.info("disable", "Stopping smoker")
        try:
            GPIO.output(Outputs.SmokeDevice.GPIO_SMOKE_MACHINE_ENABLE, 0)
        except Exception as e:
            self.logger.error_with_exception("stop", "Error while stopping!", e)
            pass

    # Run the smoker for a given time in seconds
    async def run_for(self, time: int):
        self.logger.info("run_for", "Smoker shall run for "+str(time)+" s")
        self.enable()
        await aio.sleep(time)
        self.disable()
