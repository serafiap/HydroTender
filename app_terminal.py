import threading
import sys
import platform, os

import worker
import telegram_bot

from TerminalPages import calibrationPage, sensorPage, statusPage

def clearTerminal():
    system = platform.system()
    if system == 'Linux':
        try:
            os.system("clear")
        except:
            pass
    if system == "Windows":
        try:    
            os.system("cls")
        except:
            pass

w = worker.workerThread(1, "thred")
w.setDaemon(True)
w.start()
telegram_bot.setWorker(w)

while True:
    clearTerminal()
    print("Select an option:\n")
    print("1: System Status")
    print("2: List Sensors")
    print("3: Calibrate Sensor")
    print("x: Exit")
    print("")
    selection = input("> ")

    clearTerminal()
    if selection == "1":
        statusPage.Display(w)
    elif selection == "2":
        sensorPage.Display(w)
    elif selection == "3":
        calibrationPage.Display()
    elif selection == "x":
        quit()

#w.program = worker.Program.NONE
#lightPin = worker.work_request(worker.JobType.SET_PINMODE)
#lightPin.Pin = 11
#lightPin.Mode = PinMode.OUTPUT
#w.add_job(lightPin)