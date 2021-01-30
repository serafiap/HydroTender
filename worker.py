import threading
import time
import datetime
from Serial_Arduino import *
from Serial_Arduino import SerialArduino
from tkinter import *
from enum import Enum
from typing import List
import arduino_inputs as a_i
import sensors

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
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.arduino = SerialArduino()
        
        self.WorkQueue:List[work_request] = []
        self.SensorQueue:List[int] = []
        self.program = Program.NONE
        self.AirTemp = 0
        self.Humidity = 0
        self.ReservoirTemp = 0
        self.PH = 0
        self.Concentration = 0
        self.WaterLevel = 0

        self.active = True

    def run(self):
        self.arduino.port = self.arduino.findPort()
        self.arduino.Start()
        #self.sensors = sensors.Initialize(self.arduino)
        self.sensors = sensors.ReadList(self.arduino)
        while True:
            if self.active == False:
                continue
            if(len(self.WorkQueue) > 0):
                self.execute_job(self.WorkQueue.pop(0))
            if(len(self.SensorQueue) > 0):
                sensor = self.sensors[self.SensorQueue.pop(0)]
                self.readAndProcess(sensor)
            for sensor in self.sensors:
                if sensor.ready():
                    self.readAndProcess(sensor)
            time.sleep(1)
    
    def readAndProcess(self, sensor:a_i.ArduinoReadable):
        readResult =  sensor.read()
        if readResult.resultCode == "1":
            if sensor.sensorType == a_i.SensorTypes.DHT11:
                self.AirTemp = sensor.value[0]
                self.Humidity = sensor.value[1]
            if sensor.sensorType == a_i.SensorTypes.WATER_TEMPERATURE:
                self.ReservoirTemp = sensor.value
            if sensor.sensorType == a_i.SensorTypes.WATER_CONDUCTIVITY:
                self.Concentration = sensor.value
            if sensor.sensorType == a_i.SensorTypes.WATER_LEVEL:
                self.WaterLevel = sensor.value

    def add_job(self, request:work_request):
        self.WorkQueue.append(request)

    def execute_job(self, job:work_request):
        if job.JobType == JobType.SET_PINMODE:
            self.arduino.pinMode(job.Pin, job.Mode)
        elif job.JobType == JobType.DIGITAL_WRITE:
            self.arduino.digitalWrite(job.Pin, job.DValue)




