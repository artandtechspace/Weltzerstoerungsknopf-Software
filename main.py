from core.CoreData import CoreData

import threading
from MainProgram import MainProgram
from webserver.WebProgram import run_web_thread

# Creates the core
core = CoreData()
# and main program
prog = MainProgram()


def main():
    t_serv = threading.Thread(target=run_web_thread, args=(prog,core))
    t_prog = threading.Thread(target=prog.start_thread, args=(core,))

    t_serv.start()
    t_prog.start()

    t_prog.join()
    t_serv.join()

    print("\nStarted all and everything")


main()
