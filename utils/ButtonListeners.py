from loggingsystem.Logger import Logger
import asyncio as aio
from utils.GPIOUtil import is_pressed

# Only a data class
class ButtonState:
    def __init__(self, pin: (int, bool), required: bool):
        self.pin = pin
        self.required = required

'''
A listener that checks multiple buttons and return once one reaches the required state
'''
class ButtonListener:

    logger = Logger("ButtonListener")

    def __init__(self):
        self.registered_states : [ButtonState] = []
        pass

    '''
    Adds a new button with the state it must reach to continue
    required = true means pressed, false means unpressed
    
    :return a unique id per registered state to later compare with which state did trigger
    '''
    def wait_for_change(self, pin: (int, bool), to: bool = True):
        # Registers the button state
        state = ButtonState(pin, to)
        self.registered_states.append(state)

        return self

    '''
    Async method to wait until any of the registered buttons reaches the required state
    '''
    async def then(self):
        # Ensures at least one button has been registered
        if len(self.registered_states) <= 0:
            self.logger.error("wait_for_any_change","No button states have been registered")

        # Waits for a state change
        while True:
            # Checks every registered state
            for state in self.registered_states:
                # Checks the button state
                if is_pressed(state.pin) == state.required:
                    return state.pin


            await aio.sleep(0.2)


