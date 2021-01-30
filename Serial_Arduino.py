import enum
import serial, time, datetime
from enum import Enum
from serial.tools import list_ports

class PinMode(Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT" 

class DigitalValue(Enum):
    HIGH = "HIGH"
    LOW = "LOW"

class DHT(Enum):
    DHT11 = "DHT11"
    DHT22 = "DHT22"

class SerialArduino:
    Initialized = False
    connection = serial.Serial()



    def __init__(self, port = "", baud = 115200):
        self.port = port
        self.baud = baud

    def findPort(self, baud = 115200) -> str:
        ports = list_ports.comports()
        self.baud = baud
        connection = serial.Serial()
        timeout = 0.5
        for port in ports:
            #try:
                self.port = port.device
                self.Start()

                #connection = serial.Serial(port.device, 115200)

                start = datetime.datetime.now()
                response = self.confirm()
                self.connection.close()
                if response == "1":
                    return port.device
                else:
                    continue
                while True:
                    data = connection.readline()[:-2]
                    if data == "1":
                        return port.device
                    if (datetime.datetime.now() - start).total_seconds() >= timeout:
                        continue
            #except Exception:
            #    continue

    def Start(self, delay = 3):
        self.connection = serial.Serial(self.port, self.baud)
        self.connection.timeout = 0.1
        time.sleep(delay)

    def Clear(self):
        self.connection.read_all()

    def confirm(self):
        self.Clear()
        self.connection.write(self.__confirm())
        return self.__AwaitResponse()

    def pinMode(self, pin:int, mode: PinMode):
        self.Clear()
        self.connection.write(self.__pinMode(pin, mode))
        return self.__AwaitResponse()

    def analogWrite(self, pin:int, val:int, duration:int = -1):
        self.Clear()
        self.connection.write(self.__analogWrite(pin, val, duration))
        return self.__AwaitResponse()

    def digitalWrite(self, pin:int, val:DigitalValue, duration:int = -1):
        self.Clear
        self.connection.write(self.__digitalWrite(pin, val, duration))
        return self.__AwaitResponse()

    def analogRead(self, pin:int):
        self.Clear()
        self.connection.write(self.__analogRead(pin))
        return self.__AwaitResponse()

    def digitalRead(self, pin:int):
        self.Clear
        self.connection.write(self.__digitalRead(pin))
        return self.__AwaitResponse()

    def dhtInitialize(self, pin:int, dhtType:DHT):
        self.Clear
        self.connection.write(self.__dhtInitialize(pin, dhtType))
        return self.__AwaitResponse()

    def dhtTemperature(self, index:int):
        self.Clear
        self.connection.write(self.__dhtTemperature(index))
        return self.__AwaitResponse()

    def dhtHumidity(self, index:int):
        self.Clear()
        self.connection.write(self.__dhtHumidity(index))
        return self.__AwaitResponse()

    def dht(self, pin:int, dhtType:DHT):
        self.Clear()
        self.connection.write(self.__dht(pin, dhtType))
        return self.__AwaitResponse()

    def idDS18B20(self, pin:int):
        self.Clear()
        self.connection.write(self.__idDS18B20(pin))
        return self.__AwaitResponse()

    def readByAddressDS18B20(self, pin:int, address):
        self.Clear()
        self.connection.write(self.__addressDS18B20(pin, address))
        return self.__AwaitResponse()

    def firstDS18B20(self, pin:int):
        self.Clear()
        self.connection.write(self.__firstDS18B20(pin))
        return self.__AwaitResponse()

    def ultrasonic(self, triggerPin:int, echoPin:int):
        self.Clear()
        self.connection.write(self.__ultrasonic(triggerPin, echoPin))
        return self.__AwaitResponse()

    def __AwaitResponse(self, timeout = 10):
        start = datetime.datetime.now()
        while True:
            data = self.connection.readline()[:-2]
            if data:
                if data.decode("utf-8").split(";")[0] == "0":
                    start = datetime.datetime.now()
                else:
                    return (data.decode("utf-8"))
            if (datetime.datetime.now() - start).total_seconds() >= timeout:
                return -100

    def __confirm(self):
        return str.encode("confirm*")

    def __pinMode(self, pin:int, mode:PinMode):
        return str.encode("pinMode;{};{}*".format(pin, mode.value))

    def __digitalWrite(self, pin: int, val: DigitalValue, seconds: int = -1):
        return str.encode("digitalWrite;{};{};{}*".format(pin, val.value, seconds))

    def __analogWrite(self, pin: int, val: int, seconds: int = -1):
        return str.encode("analogWrite;{};{};{}*".format(pin,val, seconds))

    def __digitalRead(self, pin: int):
        return str.encode("digitalRead;{}*".format(pin))

    def __analogRead(self, pin: int):
        return str.encode("analogRead;{}*".format(pin))

    def __dhtInitialize(self, pin: int, dhtType: DHT):
        return str.encode("startDHT;{};{}*".format(pin, dhtType))

    def __dhtTemperature(self, index:int):
        return str.encode("readDHTT;{}*".format(index))

    def __dhtHumidity(self, index:int):
        return str.encode("readDHTH;{}*".format(index))

    def __dht(self, pin:int, dhtType:DHT):
        return str.encode("readDHT;{};{}*".format(pin, dhtType.value))

    def __idDS18B20(self, pin:int):
        return str.encode("idDS18B20;{}*".format(pin))

    def __addressDS18B20(self, pin:int, address):
        return str.encode("addressDS18B20;{};{}*".format(pin, address))

    def __firstDS18B20(self, pin:int):
        return str.encode("firstDS18B20;{}*".format(pin))

    def __ultrasonic(self, triggerPin:int, echoPin:int):
        return str.encode("ultrasonic;{};{}*".format(triggerPin, echoPin))





    
