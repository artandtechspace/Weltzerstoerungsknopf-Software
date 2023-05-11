from core.CoreData import CoreData
import asyncio as aio
from enum import Enum
from peripherals.tests.PeripheralTestHand import on_hand_test
from peripherals.tests.PeripheralTestSmoker import on_smoker_test
from peripherals.tests.PeripheralTestLeds import on_leds_test
from peripherals.tests.PeripheralTestPrinter import on_printer_test
from peripherals.tests.PeripheralTestScissors import on_scissors_test

'''
The devices are order in the followin way:
(
    name: str,
    infotext: str | None (Text to display when this test is starting),
    icon: str (Icon to display inside the web-interface)
    callback: Callback (Function to execute when the start starts)
)
'''


class PeripheralTestType(Enum):
    SCISSORS = (
        "Scissors",
        None,
        "mdi-content-cut",
        on_scissors_test
    )
    PRINTER = (
        "Printer",
        None,
        "mdi-printer-outline",
        on_printer_test
    )
    LEDS = (
        "Leds",
        None,
        "mdi-led-variant-outline",
        on_leds_test
    )
    SMOKER = (
        "Smoker",
        None,
        "mdi-fire",
        on_smoker_test
    )
    HAND = (
        "Hand",
        "Test will start once you switch the 'PRIMED'-Switch into it's upper position",
        "mdi-hand-peace",
        on_hand_test
    )

# Returns a given test as a json-object to send over the network
def as_json(test: PeripheralTestType):
    return {
        "subtext": test.value[1],
        "icon": test.value[2]
    }

# Takes in a peripheral-test-type and returns its corresponding function
def get_Function(test: PeripheralTestType):
    return test.value[3]
