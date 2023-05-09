from core.CoreData import CoreData
import asyncio as aio
from loggingsystem.Logger import Logger


# Tests the smoker
async def on_smoker_test(logger: Logger, core: CoreData):
    logger.debug("on_smoker_test", "starting test, running smoker for 1 second")
    # TODO: Implement test.png image
    core.smoker.enable("This is a printer-test", "test.png")
    await aio.sleep(1)
    core.smoker.disable()
    logger.debug("on_smoker_test", "ending test")
