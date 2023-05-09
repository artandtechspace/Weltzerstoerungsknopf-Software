from loggingsystem.Logger import Logger
from escpos.printer import Usb
from peripherals.PeripheralConfig import Outputs


class PrinterDevice:
    logger = Logger("PrinterDevice")

    def __init__(self):
        # If the program knows that the printer isn't connected
        self.__is_dead = True
        # Printer instance
        self.__printer = None
        self.__reconnect_printer()

    # Tries to connect the printer
    def __reconnect_printer(self):
        self.logger.debug("__reconnect_printer","Printer is reconnecting...")

        self.__is_dead = True
        try:
            # Tries to connect the printer
            self.__printer = Usb(Outputs.Printer.VENDOR_ID, Outputs.Printer.PRODUCT_ID, 0, 4, 0x03)
            self.__is_dead = False
        except Exception as e:
            self.logger.error("__reconnect_printer",("No printer found, retrying next time a printjob get's send", e))

    '''
    Takes in the
    :param text as the infotext and a path
    :image to the image that shall be printed
    
    If the printer is disconnect, it wont print (duh) but as soon as the next job comes through it will
    '''

    def print_preset(self, text: str, image: str):
        # Will fist try to connect to the printer if it knows that he is disconnected
        if self.__is_dead:
            self.__reconnect_printer()
        try:
            # Prints...
            # - the info text
            self.__printer.text(text)
            self.__printer.text("\n")

            # - the image
            self.__printer.image(image)
            self.__printer.text("\n")
            # Finishes the print
            self.__printer.cut()

            return
        except Exception as e:
            self.logger.error("print_preset", ("Printing failed, trying to reconnect printer...", e))
            self.__reconnect_printer()
