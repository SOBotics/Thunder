#!/usr/bin/python
import chatexchange
import time
import string
import pickle

botsList = [{"name": "", "user_id": -1, "to_ping": "", "time_to_wait": 900, "last_message_time": time.time(), "rooms": [], "status": ""}]

def addBot (name, user_id, to_ping, rooms, time_to_wait=900, last_message_time=time.time(), status="alive"):
    botsList.append ({"name": name, "user_id": user_id, "to_ping": to_ping, "time_to_wait": time_to_wait, "last_message_time": last_message_time, "rooms": rooms, "status": status})

def updateLastMessageTime (userID):
    for each_bot in botsList:
        if each_bot ["user_id"] == userID:
            each_bot ["last_message_time"] = time.time()
            each_bot ["status"] = "alive"
            break

def updateTimeToWait (userID, timeToWait):
    for each_bot in botList:
        if each_bot ["user_id"] == userID:
            each_bot ["time_to_wait"] = timeToWait
            break

def deleteBot (userID):
    for each_bot in botList:
        if each_bot ["user_id"] == userID:
            botList.remove (each_bot)

def isBotAlive (userID):
    alive = False

    for each_bot in botsList:
        if each_bot ["user_id"] == userID:
            if time.time() - each_bot ["last_message_time"] < each_bot ["time_to_wait"]:
                alive = True

    return alive
