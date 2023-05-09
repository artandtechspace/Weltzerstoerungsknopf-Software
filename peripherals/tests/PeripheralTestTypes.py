from core.CoreData import CoreData
import asyncio as aio
from enum import Enum

async def on_scissors_test(core: CoreData):
    print("Testing some stuff, now sleeping for 111s")
    await aio.sleep(111)


class DeviceTestType(Enum):
    SCISSORS = on_scissors_test