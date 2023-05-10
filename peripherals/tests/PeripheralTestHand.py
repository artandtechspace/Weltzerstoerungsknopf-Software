from core.CoreData import CoreData
from loggingsystem.Logger import Logger
from utils.ButtonListeners import ButtonListener
from peripherals.PeripheralConfig import Inputs

# Tests the hand
async def on_hand_test(logger: Logger, core: CoreData):
    logger.debug("on_hand_test", "=== starting test, will now wait for open prime-switch")

    await ButtonListener()\
        .wait_for_change(Inputs.Buttons.GPIO_PRIME_SWITCH)\
        .then()

    logger.debug("on_hand_test","prime-switch found as open, start moving")

    await core.hand.move_outside()
    await core.hand.move_inside()
    logger.debug("on_hand_test", "=== ending test")
