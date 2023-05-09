from core.CoreData import CoreData
import asyncio as aio
from loggingsystem.Logger import Logger


# Tests the scissors
async def on_scissors_test(logger: Logger, core: CoreData):
    logger.debug("on_scissors_test", "starting test")
    await core.scissors.close()
    await core.scissors.open()
    logger.debug("on_scissors_test", "ending test")
