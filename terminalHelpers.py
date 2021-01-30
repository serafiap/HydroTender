import platform, os



def clearTerminal():
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