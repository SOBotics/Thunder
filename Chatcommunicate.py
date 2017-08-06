#!/usr/bin/python
import chatexchange
import Utilities
import string
import threading
import string
from Commands import commandList
import TrackBots
import QuietRooms
import time

runningCommands = list()

def runCommand (command, message, args):
    commandThread = threading.Thread (target=commandList[command], args=(message, args), kwargs={})
    
    runningCommands.append ({"thread": commandThread, "command": command, "user": message.user.name})
    commandThread.start()

def handleCommand (content, message):
    if len (content) == 0:
        return

    #Remove any punctuation from the string (https://stackoverflow.com/a/266162/4688119)
    for i in range (len (content)):
        content [i] = content [i].translate (string.punctuation)

    args = list ()

    for command, callback in commandList.items():
        usageComponents = command.split()
        args = []
        match = True
        lastIndex = min (len(content), len(usageComponents))

        for i in range (lastIndex):
            component = content [i]
            usageComponent = usageComponents [i]

            if usageComponent == '*':
                args.append (component)
            elif usageComponent == '...':
                #Everything else is arguments; add them to the list
                temp = i
                while temp < len(content):
                    args.append (content [temp])
                    temp += 1
            elif component != usageComponent:
                match = False

        minCount = (len(usageComponents) - 1) if (usageComponents[-1] == '...') else len(usageComponents)
        if len(content) < minCount:
            match = False

        if match == True:
            runCommand(command, message, args)

def handleMessage (message, client):
    if not isinstance (message, chatexchange.events.MessagePosted):
        #Ignore non-message_posted events
        return
    
    try:
        print ("%s: %s" % (message.user.name, message.content))
    except UnicodeEncodeError as err:
        print ("Unicode error occurred: " + str (err))

    if message.user.id == Utilities.myUserID:
        Utilities.lastMessageTime = time.time()

    for each_bot in TrackBots.bots_list:
        if each_bot.user_id == message.user.id:
            each_bot.update_last_message_time(time.time())

    if QuietRooms.is_room_quiet(message.room.id):
        return
    
    try:
        content = message.content.lower()
    except AttributeError as attErr:
        print ("Attribute error occurred: ")
        print (attErr)
        return

    content = content.split ()
    
    shortName = Utilities.name [:-(len (Utilities.name) - Utilities.minNameCharacters)]

    if content [0].startswith (shortName.lower()):
        del content [0]
        handleCommand (content, message)

