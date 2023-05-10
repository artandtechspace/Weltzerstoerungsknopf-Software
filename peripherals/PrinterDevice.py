from loggingsystem.Logger import Logger
from escpos.printer import Usb
from peripherals.PeripheralConfig import Outputs
import pathlib


class PrinterDevice:
    # Path to the resource-folder
    rsc_path = str(pathlib.Path(__file__).parent.absolute()) + "/../rsc/images/"

    logger = Logger("PrinterDevice")

    def __init__(self):
        # If the program knows that the printer isn't connected
        self.__is_dead = True
        # Printer instance
        self.__printer = None
        self.__reconnect_printer()

    # Tries to connect the printer
    def __reconnect_printer(self):
        self.logger.debug("__reconnect_printer", "Printer is reconnecting...")

        self.__is_dead = True
        try:
            # Tries to connect the printer
            self.__printer = Usb(Outputs.Printer.VENDOR_ID, Outputs.Printer.PRODUCT_ID, 0, 4, 0x03)
            self.__is_dead = False
        except Exception as e:
            self.logger.warn_exception("__reconnect_printer", "No printer found, retrying next time a printjob get's "
                                                              "send", e)

    '''
    Takes in the
    :param text as the infotext and a path
    :image to the image that shall be printed
    
    If the printer is disconnect, it wont print (duh) but as soon as the next job comes through it will
    '''

    def print_preset(self, text: str, image: str):
        self.logger.info("print_preset", "Starting to print")
        # Will fist try to connect to the printer if it knows that he is disconnected
        if self.__is_dead:
            self.__reconnect_printer()
        try:
            # Prints...
            # - the info text
            self.__printer.text("\n"+text+"\n")

            # - the image
            self.__printer.image(self.rsc_path+image)
            self.__printer.text("\n")
            # Finishes the print
            self.__printer.cut()

            return
        except Exception as e:
            self.logger.warn_exception("print_preset", "Printing failed, trying to reconnect printer", e)
            self.__reconnect_printer()
