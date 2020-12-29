import threading
from tkinter.font import families
import serial
import time
import datetime
import sys
from tkinter import *
from tkinter import ttk
import arduino_strings as a_s
import ui_logic as uil
from Serial_Arduino import SerialArduino
from Serial_Arduino import PinMode
import worker
import shared_resources as sr



############################################################
# EVENTS
############################################################


def update(*args):
    #(arduino.analogWrite(11, newVal.get()))
    sr.volumeQueue.append( int(newVal.get()))
    newVal.set("")

def increment(*args):
    sr.increment = True

def decrement(*args):
    sr.increment = False

def handle_exit(event):
    sr.workerKilled = True
    sys.exit()


arduino = SerialArduino("COM4", 115200)
arduino.Start(2)
print(arduino.pinMode(11, PinMode.OUTPUT))
root = Tk()
w = worker.workerThread(1, "thred", arduino)

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
ttk.Label(mainframe, textvariable=w.volume, text = "0").grid(column=2, row=2, sticky=(W,E))

ttk.Button(mainframe, text="Up", command=increment).grid(column=1, row=3, sticky=(N, W, E, S))
ttk.Button(mainframe, text="Down", command=decrement).grid(column=2, row=3, sticky=(N, W, E, S))
ttk.Button(mainframe, text = "Update", command=update).grid(column=3, row=3, sticky=(N, W, E, S))

ttk.Label(mainframe,text="New Value:").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Current Value:").grid(column=1, row=2, sticky=E)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

############################################################
# Bindings
############################################################


root.bind("<Return>", update)
root.bind("<Escape>", handle_exit)



#window.attributes('-fullscreen', True)
# window.state('zoomed')
w.start()

root.mainloop()
