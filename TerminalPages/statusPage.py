import enum
from tkinter.constants import TRUE
import worker
import threading
import time
import terminalHelpers
from enum import Enum

class Options(Enum):
    QUIT = "x"
    REFRESH = "1"

class Display():
    
    def __init__(self, w:worker.workerThread):
        self.wrkr = w
        self.threadAlive = False
        self.refreshDue = True
        statusThread = threading.Thread(target=self._MainDisplay)
        statusThread.start()
        while self.refreshDue:
            time.sleep(0.1)
            pass
        while True:
            inp = input("> ")
            if inp == Options.REFRESH.value:
                self.refreshDue = True
                while self.refreshDue:
                    time.sleep(0.1)
                    pass
            if inp == Options.QUIT.value:
                self.threadAlive = False
                break
        pass

    def _MainDisplay(self):
        self.threadAlive = True
        startTime = time.time()
        refreshSeconds = 15
        while self.threadAlive:
            if (time.time() - startTime) > refreshSeconds:
                self.refreshDue = True
            if self.refreshDue:
                terminalHelpers.clearTerminal()
                print("System Status")
                print("-------------")
                print()
                print("Air Temperature: {}".format(self.wrkr.AirTemp))
                print("Reservoir temp: {}".format(self.wrkr.ReservoirTemp))
                print("Water Level: {}".format("Lvl"))
                print("Concentration: {}".format(int(self.wrkr.Concentration)))
                print("ph: {}".format(self.wrkr.PH))
                print("-------------")
                print("\n")
                print("Select option:")
                print("{}: Refresh date".format(Options.REFRESH.value))
                print("{}: Return to main screen".format(Options.QUIT.value))
                startTime = time.time()
                self.refreshDue = False
