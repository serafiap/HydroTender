import threading
import time
import datetime
from Serial_Arduino import *
from Serial_Arduino import SerialArduino
from tkinter import *
import shared_resources as sr
from enum import Enum
from typing import List

class Program(Enum):
    NONE = 0
    DHT = 4
    DS18B20 = 5

class JobType(Enum):
    SET_PINMODE = 0
    DIGITAL_WRITE = 1
    DIGITAL_READ = 2
    ANALOG_WRITE = 3
    ANALOG_READ = 4
    DHT_READ = 5
    DS18B20_IDENTIFY = 6
    DS18B20_READ = 7

class work_request():
    def __init__(self, jobType:JobType):
        self.JobType:JobType = jobType
        self.Pin:int
        self.AValue:int
        self.DValue:DigitalValue
        self.Type:DHT
        self.Mode:PinMode

class workerThread (threading.Thread):
    def __init__(self, threadID, name, arduino: SerialArduino):
        threading.Thread.__init__(self)
        self.arduino = arduino
        self.WorkQueue:List[work_request] = []
        self.volume = StringVar()
        self.volume.set(0)
        self.program = Program.NONE

    def run(self):
        sr.workerRunning = True
        while sr.workerKilled == False:
            if(len(self.WorkQueue) > 0):
                self.execute_job(self.WorkQueue.pop(0))
            self.dht_test()
            self.DS18B20_test()
        self.end()

    def add_job(self, request:work_request):
        self.WorkQueue.append(request)

    def dht_test(self):
        while sr.workerKilled == False and self.program == Program.DHT:
            result = self.arduino.dht(8, DHT.DHT11)
            temp = result.split(";")[1]
            humi = result.split(";")[2]
            print(result)
            print("Temp: {}, Humidity: {}".format(temp, humi))
            time.sleep(5)

    def DS18B20_test(self):
        while sr.workerKilled == False and self.program == Program.DS18B20:
            address = self.arduino.idDS18B20(2).split(';')[1]
            print(address)
            time.sleep(2)
            temp = (self.arduino.addressDS18B20(2, address))
            self.volume.set(temp.split(";")[1])
            time.sleep(5)

    def execute_job(self, job:work_request):
        if job.JobType == JobType.SET_PINMODE:
            self.arduino.pinMode(job.Pin, job.Mode)
        elif job.JobType == JobType.DIGITAL_WRITE:
            self.arduino.digitalWrite(job.Pin, job.DValue)

    def end(self):
        sr.workerRunning = False


