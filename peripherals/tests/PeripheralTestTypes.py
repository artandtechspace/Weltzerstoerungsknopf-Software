from core.CoreData import CoreData
import asyncio as aio
from enum import Enum
from peripherals.tests.PeripheralTestHand import on_hand_test
from peripherals.tests.PeripheralTestSmoker import on_smoker_test
from peripherals.tests.PeripheralTestLeds import on_leds_test
from peripherals.tests.PeripheralTestPrinter import on_printer_test
from peripherals.tests.PeripheralTestScissors import on_scissors_test


class PeripheralTestType(Enum):
    SCISSORS = ("Scissors", on_scissors_test)
    PRINTER = ("Printer", on_printer_test)
    LEDS = ("Leds", on_leds_test)
    SMOKER = ("Smoker", on_smoker_test)
    HAND = ("Hand", on_hand_test)
