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

############################################################
# EVENTS
############################################################


def handle_click(*args):
    (arduino.analogWrite(11, newVal.get()))
    currentVal.set(newVal.get())
    newVal.set("")


def handle_exit(event):
    sys.exit()


arduino = SerialArduino("COM4", 9600)
arduino.Start(2)
print(arduino.pinMode(11, PinMode.OUTPUT))


############################################################
# Geometry
############################################################

root = Tk()
root.title("Adjust LED")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=0)
root.rowconfigure(0, weight=0)

newVal = StringVar()
val_entry = ttk.Entry(mainframe, width=7, textvariable=newVal)
val_entry.grid(column=2, row=1,sticky=(W,E))
val_entry.focus()

currentVal= StringVar()
ttk.Label(mainframe, textvariable=currentVal, text = "0").grid(column=2, row=2, sticky=(W,E))

ttk.Button(mainframe, text = "Update", command=handle_click).grid(column=3, row=3, sticky=W)
ttk.Label(mainframe,text="New Value:").grid(column=1, row=1, sticky=E)
ttk.Label(mainframe, text="Current Value:").grid(column=1, row=2, sticky=E)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

############################################################
# Bindings
############################################################


root.bind("<Return>", handle_click)
root.bind("<Escape>", handle_exit)



#window.attributes('-fullscreen', True)
# window.state('zoomed')
root.mainloop()
