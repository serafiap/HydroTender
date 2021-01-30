import worker
import terminalHelpers
from enum import Enum

class Options(Enum):
    EXIT = "x"
    pass

class Display():
    def __init__(self, w:worker.workerThread):
        self.wrkr = w
        while True:
            terminalHelpers.clearTerminal()
            print("Select sensor to read")
            print("---------------------")
            for x in range(len(w.sensors)):
                print("{}: {}".format(x, w.sensors[x].sensorType.name))
            print("{}: Return to main menu".format(Options.EXIT.value))
            selection = input("> ")
            if selection == Options.EXIT.value:
                break
            try:
                terminalHelpers.clearTerminal()
                selection = int(selection)
                w.SensorQueue.append(selection)
                print ("Sensor {} added to queue".format(selection))
                input()
            except:
                pass