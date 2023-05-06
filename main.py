import asyncio as aio
from core.CoreData import CoreData
from core.states.ResetState import start_reset_state
from Logger import Logger

async def main():
    logger = Logger("Main")

    # Creates the core
    core = CoreData()

    # Current state
    state = start_reset_state

    while True:
        logger.debug("main", "Starting state "+str(state.__name__))
        # Executes and updates the state
        state = await state(core)

aio.run(main())