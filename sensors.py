import arduino_inputs as a_i
from Serial_Arduino import *
from Serial_Arduino import SerialArduino

def Initialize(arduino: SerialArduino):
    list = [
        #a_i.DHT11(arduino, 7, 1),
        a_i.WaterTemperature(arduino, 8, readIntervalMinutes=1),
        a_i.WaterConductivity(arduino, 7, 14, 6, (60*24))
    ]
    return list

def ReadList(arduino:SerialArduino):
    list = [ ]
    dht11 = GetCSVData("sensors/DHT11.csv","Pin,ReadIntervalMinutes")
    waterTemperature = GetCSVData("sensors/WaterTemperature.csv","Pin,ReadIntervalMinutes")
    waterConductivity = GetCSVData("sensors/WaterConductivity.csv","PowerPin,ReadPin,ReadCount,ReadIntervalMinutes")
    waterUltrasonicLevel = GetCSVData("sensors/WaterUltrasonicLevel.csv","TriggerPin,EchoPin,ReadIntervalMinutes")

    for x in range (1, len(dht11)):
        y = dht11[x]
        list.append(a_i.DHT11(arduino, int(y[0]), int(y[1])))

    for x in range (1, len(waterTemperature)):
        y = waterTemperature[x]
        list.append(a_i.WaterTemperature(arduino, int(y[0]), readIntervalMinutes=int(y[1])))

    for x in range (1, len(waterConductivity)):
        y = waterConductivity[x]
        list.append(a_i.WaterConductivity(arduino, int(y[0]), int(y[1]), int(y[2]), int(y[3])))
    
    for x in range (1, len(waterUltrasonicLevel)):
        y = waterUltrasonicLevel[x]
        list.append(a_i.UltrasonicWaterLevel(arduino, int(y[0]), int(y[1]), int(y[2])))
    
    return list

def GetCSVData (file:str, header:str):
    try:
        f = open(file, "r+")
    except:
        f = open(file, "w+")
    lines = f.readlines()
    fullSplit = []
    if len(lines) == 0:
        f.write(header)
    for x in lines:
        fullSplit.append(x.split(','))
    return fullSplit