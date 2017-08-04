#!/usr/bin/python
import chatexchange
import time
import string
import pickle
import Utilities

"""
botsList = [{"name": "", "user_id": -1, "to_ping": "", "time_to_wait": 900, "last_message_time": time.time(), "rooms": [], "status": ""}]
#botsList = list()

def addBot (name, user_id, to_ping, rooms, time_to_wait=900, last_message_time=time.time(), status="alive"):
    botsList.append ({"name": name, "user_id": user_id, "to_ping": to_ping, "time_to_wait": time_to_wait, "last_message_time": last_message_time, "rooms": rooms, "status": status})
"""
"""
def updateLastMessageTime (userID):
    for each_bot in botsList:
        if each_bot ["user_id"] == userID:
            print ("Last message time for userID '" + str (each_bot["user_id"]) + "' has been updated.")
            each_bot ["last_message_time"] = time.time()
            each_bot ["status"] = "alive"
            break

def updateTimeToWait (userID, timeToWait):
    for each_bot in botList:
        if each_bot ["user_id"] == userID:
            each_bot ["time_to_wait"] = timeToWait
            break

def deleteBot (userID):
    for each_bot in botsList:
        if each_bot ["user_id"] == userID:
            botsList.remove (each_bot)

def isBotAlive (userID):
    alive = False

    for each_bot in botsList:
        if each_bot ["user_id"] == userID:
            if time.time() - each_bot ["last_message_time"] < each_bot ["time_to_wait"]:
                alive = True

    return alive

def getBotIndexByID (userID):
    for i in range (len (botsList)):
        if botsList [i]["user_id"] == userID:
            return i

    return -1

def saveBotList ():
    Utilities.saveToPickle ("bot_list.pickle", botsList)

def loadBotList ():
    return Utilities.loadFromPickle ("bot_list.pickle")
"""

bots_list = []

def add_bot(name, user_id, to_ping, rooms, time_to_wait=900, last_message_time=time.time(), alive=True):
    bots_list.append (TrackBot (name, user_id, to_ping, rooms, time_to_wait, last_message_time, alive))

def get_bot(user_id):
    for each_bot in bots_list:
        if each_bot.user_id == user_id:
            return each_bot

    #TODO: Throw an error.
    return each_bot

def delete_bot(user_id):
    for each_bot in bots_list:
        if each_bot.user_id == user_id:
            bots_list.remove (each_bot)

def save_bot_list():
    dict_list = list()

    try:
        for each_class in bots_list:
            dict_list.append({"name": each_class.name, "user_id": each_class.user_id, "to_ping": each_class.to_ping, "rooms": each_class.rooms, "time_to_wait": each_class.time_to_wait, "last_message_time": each_class.last_message_time, "alive": each_class.alive})
    except AttributeError as attrerr:
        print ("Attriibute error occurred: " + str (attrerr))

    Utilities.saveToPickle("botlist.pickle", dict_list)

def load_bot_list():
    dict_list = Utilities.loadFromPickle("botlist.pickle")

    for each_dict in dict_list:
        add_bot(each_dict["name"], each_dict["user_id"], each_dict["to_ping"], each_dict["rooms"], each_dict["time_to_wait"], each_dict["last_message_time"], each_dict["alive"])

class TrackBot:
    def __init__(self, name, user_id, to_ping, rooms, time_to_wait=900, 
            last_message_time=time.time(), alive=True):
        self.name = name
        self.user_id = user_id
        self.to_ping = to_ping
        self.rooms = rooms
        self.time_to_wait = time_to_wait
        self.last_message_time = last_message_time
        self.alive = alive

    def update_time_to_wait(self, time_to_wait):
        self.time_to_wait = time_to_wait

    def update_last_message_time(self, last_message_time=Utilities.get_current_time()):
        self.last_message_time = last_message_time
        print("Updating last message time for userid " + str(self.user_id) + ".")

    def update_to_ping(self, to_ping):
        self.to_ping = to_ping

    def get_bot_status_string(self):
        if self.alive:
            return "alive"
        elif not self.alive:
            return "dead"
        else:
            #TODO: Handle this error.
            return "unknown"

    def is_bot_alive(self):
        if time.time() - self.last_message_time > self.time_to_wait:
            return False
        return True
