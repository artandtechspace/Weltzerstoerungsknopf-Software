import asyncio as aio
from core.CoreData import CoreData
from core.states.ResetState import start_reset_state
from core.states.IdleState import start_idle_state
from loggingsystem.Logger import Logger

from typing import Callable, Coroutine
from asyncio import Task
from peripherals.tests.PeripheralTestTypes import DeviceTestType


'''
The main Program runs inside a separate thread from the webserver
'''
class MainProgram:
    logger = Logger("Main")

    def __init__(self):
        # Actual task that currently is running
        self.__current_task: Task = None  # This will be populated after the first start
        # Function-Ptr for the current task
        self.__function_ptr: Callable[[Coroutine], CoreData] = start_reset_state
        self.__test_type: None | DeviceTestType = None
        pass

    # Start-method to be executed from the separate thread
    def start_thread(self, core: CoreData):
        aio.run(self.__on_run(core))

    # Async-io start method that continuously run the next state after the previous one has finished
    async def __on_run(self, core: CoreData):
        while True:
            self.logger.debug("main", "Starting state " + str(self.__function_ptr.__name__))

            # Executes the next task
            self.__current_task = aio.create_task(self.__function_ptr(core))

            # Updates the next pointer
            self.__function_ptr = await self.__current_task

            # Checks if task got canceled
            if self.__function_ptr is None:
                self.__function_ptr = self.__on_inserted

    # Method to be run as a separate state when a test-state should be executed
    async def __on_inserted(self, core: CoreData):

        # Ensures there is a test to run
        if self.__test_type is None:
            # This should be an unreachable condition
            self.logger.error("__on_inserted", "a test was scheduled but none was found as the test-type")
        else:
            # Executes the test
            await self.__test_type(core)

        return start_reset_state

    # Can be thread-save used to insert a test while the idle-state is running
    # :returns True if the test was scheduled and False if a different state is running
    async def insert_test(self, type: DeviceTestType):
        self.__test_type = type
        # Ensures that a test is only inserted into the idle-state
        if self.__function_ptr != start_idle_state:
            return False

        # Kills the main task to indicate that a test should take place
        try:
            self.__current_task.cancel()
            await self.__current_task
        except Exception:
            pass

        return True