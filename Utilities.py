#!/usr/bin/python

import pickle
import chatexchange
import time

#The chat host
host = "stackoverflow.com"

#This will contain an array of the Class 'Room' once the bot joins the specified rooms
rooms = list()

#The index of the room in 'roomsIDs' which the bot should post errors to.
error_index = 1

#The roomIDs the bot should join
roomIDs = [111347, 123602]

myself = None
myUserID = -1
client = chatexchange.Client

#The Redunda class.
Redunda = None

#List of files to sync with Redunda.
files_to_sync = [{"name": "botlist.pickle", "ispickle": True}, {"name": "quietroomlist.pickle", "ispickle": True}]

#The bot's location. Should be something like "Ashish/MacMini" (<name>/<computer>)
location = "unknown_location"

#The name of the bot. A message must start with this name to be recognized as a command
name = "@Thunder"

#The time of my last message posted in the room.
lastMessageTime = 0

#The number of characters of the name that must be included
minNameCharacters = 4

botLink = "[Thunder](https://git.io/v7kXG)"

startLink = "[ [Thunder](https://git.io/v7kXG) ]"

#The epoch time when the bot started
startTime = 0

def saveToPickle (filename, list):
    try:
        with open (filename, 'wb') as toSave:
            pickle.dump (list, toSave)
    except IOError as err:
        print ("File Error: " + err)
    except pickle.PickleError as perr:
        print ("Pickle Error: " + perr)

def loadFromPickle (filename):
    try:
        with open (filename, "rb") as toRead:
            return pickle.load (toRead)
    except IOError as err:
        print ("File Error: " + str(err))
    except pickle.PickleError as perr:
        print ("Pickle Error: " + str(perr))
    
    return []

#This should be done using `time.time()` whenever possible, but in optional variables,
#you would need to call this function for the value to not be static.
def get_current_time():
    return time.time()
