#from python-telegram-bot
from telegram import chat
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update
from worker import work_request
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import worker
import json

def getConfig():
    file = "Config/TelegramConfig.json"
    try:
        f = open(file, "r+")
    except:
        f = open(file, "w+")
    lines = f.read()
    if lines == '':
        template = '{\n"token": "",\n"users": [""]}'
        f.write(template)
        f.close()
        return []
    else:
        configDict = json.loads(lines)
        return configDict



config = getConfig()
authorizedUsers = config["users"]
updater = Updater(token=config["token"], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

workerT = worker.workerThread("1", "")
def setWorker(w):
    global workerT
    workerT = w

def Authorize(id = "", username = ""):
    if id in authorizedUsers:
        return True
    else:
        return False

def start(update:Update, context:CallbackContext):
    if Authorize(id=str(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No")


def temperature(update:Update, context:CallbackContext):
    t = str(workerT.ReservoirTemp)
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)

def concentration(update:Update, context:CallbackContext):
    c = str(workerT.Concentration)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c)

def waterLevel(update:Update, context:CallbackContext):
    l = str(workerT.WaterLevel)
    context.bot.send_message(chat_id=update.effective_chat.id, text=l)

def status(update:Update, context:CallbackContext):
    s = "System Status:\n"
    s += "Air Temperature: {}C ({:.2f}F)\n".format(workerT.AirTemp, ((float(workerT.AirTemp)*9/5)+ 32))
    s += "Humidity: {}%\n".format(workerT.Humidity)
    s += "Reservoir Temperature: {}\n".format(workerT.ReservoirTemp)
    s += "Concentration: {}\n".format(round(workerT.Concentration,2))
    s += "/status \n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=s)
    
def menu(update:Update, context:CallbackContext):
    s = "/menu:\n"
    s += "/status\n"
    s += "/start\n"
    s += "/temp\n"
    s += "/level\n"
    s += "/conc\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=s)


dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler("temp", temperature))
dispatcher.add_handler(CommandHandler("conc", concentration))
dispatcher.add_handler(CommandHandler("level", waterLevel))
dispatcher.add_handler(CommandHandler("menu", menu))



updater.start_polling()

