import threading
import tkinter
from tkinter.font import families
import serial
import time
import datetime
import sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import arduino_strings as a_s
import ui_logic as uil
from Serial_Arduino import DigitalValue, SerialArduino
from Serial_Arduino import PinMode
import worker
import shared_resources as sr



############################################################
# EVENTS
############################################################


def update(*args):
    sr.volumeQueue.append( int(newVal.get()))
    newVal.set("")

def button1(*args):
    lightOn = worker.work_request(worker.JobType.DIGITAL_WRITE)
    lightOn.Pin = 11
    lightOn.DValue = DigitalValue.HIGH
    w.add_job(lightOn)

def button2(*args):
    lightOff = worker.work_request(worker.JobType.DIGITAL_WRITE)
    lightOff.Pin = 11
    lightOff.DValue = DigitalValue.LOW
    w.add_job(lightOff)

def handle_exit(*args):
    if messagebox.askokcancel("Quit", "Quit?"):
        sr.workerKilled = True
        w.end()
        quit()


arduino = SerialArduino("COM4", 115200)
arduino.Start(2)
print(arduino.pinMode(11, PinMode.OUTPUT))
root = Tk()
w = worker.workerThread(1, "thred", arduino)
w.setDaemon(True)
w.program = worker.Program.NONE
lightPin = worker.work_request(worker.JobType.SET_PINMODE)
lightPin.Pin = 11
lightPin.Mode = PinMode.OUTPUT
w.add_job(lightPin)

############################################################
# Geometry
############################################################


root.title("Adjust LED")
root.geometry("800x480")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
mainframe.columnconfigure(4, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)
mainframe.rowconfigure(4, weight=1)

newVal = StringVar()
val_entry = ttk.Entry(mainframe, width=7, textvariable=newVal)
val_entry.grid(column=2, row=1,sticky=(W,E))
val_entry.focus()

currentVal= StringVar()
valueLabel = ttk.Label(mainframe, textvariable=w.volume, text = "0")
valueLabel.grid(column=2, row=2, sticky=(W,E))

ttk.Button(mainframe, text="1", command=button1).grid(column=1, row=3, sticky=(N, W, E, S))
ttk.Button(mainframe, text="2", command=button2).grid(column=2, row=3, sticky=(N, W, E, S))
ttk.Button(mainframe, text = "Update", command=update).grid(column=3, row=3, sticky=(N, W, E, S))

ttk.Label(mainframe,text="New Value:").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Current Value:").grid(column=1, row=2, sticky=E)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

############################################################
# Bindings
############################################################

root.protocol('WM_DELETE_WINDOW', handle_exit)
root.bind("<Return>", update)
root.bind("<Escape>", handle_exit)
root.bind("1", button1)
root.bind("2", button2)



#root.attributes('-fullscreen', True)
#root.state('zoomed')
w.start()

root.mainloop()
