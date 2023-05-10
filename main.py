from core.CoreData import CoreData

import threading
from MainProgram import MainProgram
from webserver.WebProgram import run_web_thread
from loggingsystem.LoggingManager import LoggingManager

# Creates the core
core = CoreData()
# and main program
prog = MainProgram()


def main():
    t_serv = threading.Thread(target=run_web_thread, args=(prog,core))
    t_prog = threading.Thread(target=prog.start_thread, args=(core,))
    t_logging = threading.Thread(target=LoggingManager.start_logging_thread, args=(10,))

    t_serv.start()
    t_prog.start()
    t_logging.start()

    print("\nStarted all and everything")

    t_prog.join()
    t_serv.join()
    t_logging.join()



main()
