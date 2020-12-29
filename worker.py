import threading
import time
import datetime
import Serial_Arduino
from Serial_Arduino import SerialArduino
from tkinter import *
import shared_resources as sr

class workerThread (threading.Thread):
    def __init__(self, threadID, name, arduino:SerialArduino):
        threading.Thread.__init__(self)
        self.arduino = arduino
        self.pin = 11
        self.volume = StringVar()
        self.volume.set(0)

    def run(self):
        sr.workerRunning = True
        print("run")
        while sr.workerKilled == False:
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
        self.running = False
        