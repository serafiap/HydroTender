from enum import Enum

class PinMode(Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"

class DigitalValue(Enum):
    HIGH = "HIGH"
    LOW = "LOW"

def pinMode(pin:int, mode:PinMode):
    return str.encode("pinMode;{};{}*".format(pin, mode.value))

def digitalWrite(pin: int, val: DigitalValue, seconds: int = -1):
    if val:
        return str.encode("digitalWrite;{};{};{}*".format(pin, val.value, seconds))

def analogWrite(pin: int, val: int, seconds: int = -1):
    return str.encode("analogWrite;{};{};{}*".format(pin,val, seconds))
