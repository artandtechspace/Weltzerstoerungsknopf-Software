from core.CoreData import CoreData
import asyncio as aio
from loggingsystem.Logger import Logger


# Tests the printer
async def on_printer_test(logger: Logger, core: CoreData):
    logger.debug("on_printer_test", "=== starting test")
    core.printer.print_preset("This is a printer-test", "test.png")
    logger.debug("on_printer_test", "=== ending test")
