import os
import sys
import time
import platform

def clear():
    system = platform.system()
    if system == 'Linux':
        try:
            os.system("clear")
        except:
            pass
    if system == "Windows":
        try:    
            os.system("cls")
        except:
            pass

print(platform.system())
#os.system("dir")
time.sleep(2)
clear()
print("1")
time.sleep(2)
clear()
print("2")
time.sleep(2)
clear()
print("3")
time.sleep(2)
clear()
input()
clear()