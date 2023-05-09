from core.CoreData import CoreData
import asyncio as aio
from loggingsystem.Logger import Logger


# Tests the hand
async def on_hand_test(logger: Logger, core: CoreData):
    logger.debug("on_hand_test", "starting test")
    await core.hand.move_outside()
    await core.hand.move_inside()
    logger.debug("on_hand_test", "ending test")
