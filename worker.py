import threading
import time
import datetime
from Serial_Arduino import *
from Serial_Arduino import SerialArduino
from tkinter import *
import shared_resources as sr
from enum import Enum

class Program(Enum):
    NONE = 0
    BLINK = 1
    PULSE = 2


class workerThread (threading.Thread):
    def __init__(self, threadID, name, arduino:SerialArduino):
        threading.Thread.__init__(self)
        self.arduino = arduino
        self.pin = 11
        self.volume = StringVar()
        self.volume.set(0)
        self.program = Program.NONE

    def run(self):
        sr.workerRunning = True
        print("run")
        while sr.workerKilled == False:
            print("Working")
            self.pulse()
            self.blink()
        self.end()
            
    def blink(self):
        state = DigitalValue.LOW
        while sr.workerKilled == False and self.program == Program.BLINK:
            self.arduino.digitalWrite(11, state)
            if state == DigitalValue.HIGH:
                state = DigitalValue.LOW
            else:
                state = DigitalValue.HIGH
            time.sleep(0.1)

    def pulse(self):
        while sr.workerKilled == False and self.program == Program.PULSE:
            try:
                
                vol = int(self.volume.get())
                if len(sr.volumeQueue)>0:
                        vol = sr.volumeQueue.pop(0)
                if sr.increment:
                    if vol < 255:
                        vol += 1
                    else:
                        sr.increment = False
                else:
                    if vol > 0:
                        vol -= 1
                    else:
                        sr.increment = True
                self.volume.set(vol)
                self.arduino.analogWrite(self.pin, vol)
                #time.sleep(.00001)
                pass
            except Exception:
                pass

    def end(self):
        sr.workerRunning = False
        