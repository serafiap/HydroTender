from Serial_Arduino import *
from Serial_Arduino import SerialArduino
import datetime
import time

class SensorTypes(Enum):
    NONE = 0
    DHT11 = 1
    WATER_CONDUCTIVITY = 2
    WATER_TEMPERATURE = 3
    WATER_LEVEL = 4
    

class SensorReadingResult:
    def __init__(self):
        self.resultCode = ""
        self.resultMessage = ""
        self.results = []

    def getResult(self, result: str):
        if result != -100:
            splitResult = result.split(";")
            self.resultCode = splitResult[0]
            if len(splitResult) > 1:
                self.resultMessage = splitResult[1]
                if splitResult[0] == "1":
                    for x in splitResult[1:]:
                        self.results.append(x)


class ArduinoReadable:
    def __init__(self, readIntervalMinutes) -> None:
        self.sensorType = SensorTypes.NONE
        self.lastReading = datetime.datetime(2000,1,1)
        self.readIntervalMinutes = readIntervalMinutes
        self.active = True
        self.value = ""
        super().__init__()

    def read(self) -> SensorReadingResult:
        self.lastReading = datetime.datetime.now()
        pass

    def ready(self) -> bool:
        if datetime.datetime.now() > self.lastReading + datetime.timedelta(minutes=self.readIntervalMinutes):
            return True
        else:
            return False


class WaterConductivity(ArduinoReadable):
    def __init__(self, arduino: SerialArduino, powerPin: int, readPin: int, readCount: int, readIntervalMinutes: int):
        super().__init__(readIntervalMinutes)
        self.arduino = arduino
        self.powerPin = powerPin
        self.readPin = readPin
        self.readCount = readCount
        self.sensorType = SensorTypes.WATER_CONDUCTIVITY
        self.voltage = 0

    def read(self) -> SensorReadingResult:
        self.lastReading = datetime.datetime.now
        success = "1"
        result = SensorReadingResult()
        result.getResult(self.arduino.pinMode(self.powerPin, PinMode.OUTPUT))
        if result.resultCode != success:
            self.abort()
            return result
        result.getResult(self.arduino.pinMode(self.readPin, PinMode.INPUT))
        if result.resultCode != success:
            self.abort()
            return result
        result.getResult(self.arduino.digitalWrite(self.powerPin, DigitalValue.HIGH))
        if result.resultCode != success:
            self.abort()
            return result
        result.results = []
        for x in range(self.readCount):
            result.getResult(self.arduino.analogRead(self.readPin))
        self.abort()
        super().read()

        validResults = 0
        totalResult = 0
        for x in range(int(len(result.results)/2), len(result.results)):
            try:
                val = float(result.results[x])
                validResults += 1
                totalResult += val
            except:
                pass
        if validResults > 0:
            self.value = totalResult/validResults
            #print (result.results)
        return result

    def abort(self):
        self.arduino.digitalWrite(self.powerPin, DigitalValue.LOW)
        self.arduino.pinMode(self.powerPin, PinMode.INPUT)


class WaterTemperature(ArduinoReadable):
    def __init__(self, arduino: SerialArduino, pin: int, readIntervalMinutes:int = -1) -> None:
        super().__init__(readIntervalMinutes)
        self.arduino = arduino
        self.pin = pin
        self.sensorType = SensorTypes.WATER_TEMPERATURE

    def read(self) -> SensorReadingResult:
        result = SensorReadingResult()
        result.getResult(self.arduino.firstDS18B20(self.pin))
        if result.resultCode == "1":
            self.value = result.results[0]
        super().read()
        return result


class DHT11 (ArduinoReadable):
    def __init__(self, arduino: SerialArduino, pin: int, readIntervalMinutes:int) -> None:
        super().__init__(readIntervalMinutes)
        self.arduino = arduino
        self.pin = pin
        self.sensorType = SensorTypes.DHT11

    def read(self) -> SensorReadingResult:
        result = SensorReadingResult()
        result.getResult(self.arduino.dht(self.pin, DHT.DHT11))
        if result.resultCode == "1":
            self.value = [result.results[0], result.results[1]]
        super().read()
        return result

class UltrasonicWaterLevel(ArduinoReadable):
    def __init__(self, arduino:SerialArduino, triggerPin:int, echoPin:int, readIntervalMinutes:int) -> None:
        super().__init__(readIntervalMinutes)
        self.arduino = arduino
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        self.sensorType = SensorTypes.WATER_LEVEL

    def read(self) -> SensorReadingResult:
        result = SensorReadingResult()
        result.getResult(self.arduino.ultrasonic(self.triggerPin, self.echoPin))
        if result.resultCode == "1":
            self.value = result.results[0]
        super().read()
        return result
