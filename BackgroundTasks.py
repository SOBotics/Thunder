#!/usr/bin/python
import chatexchange
import threading
import Chatcommunicate
import time
from Utilities import rooms
import Utilities
import TrackBots
import chatexchangeExtension as ceExt
from chatexchangeExtension import postMessage, postReply
import QuietRooms

shouldShutdown = False
shouldReboot = False

def listenForMessages (client, roomIDs):
    for each_id in roomIDs:
        rooms.append (client.get_room (each_id))

    for each_room in rooms:
        each_room.join()
        print ("Joined room " + str(each_room.id) + ".")
        postMessage(each_room, Utilities.startLink + " Thunder started.")
    
        each_room.watch (Chatcommunicate.handleMessage)

    QuietRooms.quietRooms = QuietRooms.loadQuietRoomList()

    for each_room in QuietRooms.quietRooms:
        rooms.append (client.get_room (each_room ["room_id"]))
        rooms [len (rooms) - 1].join()
        print ("Joined quiet room " + str (rooms [len (rooms) - 1].id) + ".")

        rooms [len (rooms) - 1].watch_polling (Chatcommunicate.handleMessage, each_room ["interval"])

def scheduleBackgroundTasks (client, roomIDs):
    #Listen for input
    inputListener = threading.Thread (target=listenForMessages, args=(client, roomIDs), kwargs={})

    inputListener.start()
    
    botListLen = len (TrackBots.botsList)
    quietRoomLen = len (QuietRooms.quietRooms)
    
    #Load the list of bots from the pickle
    TrackBots.botsList = TrackBots.loadBotList()

    while (1):
        try:
            #Remove commands which have completed.
            if len (Chatcommunicate.runningCommands) > 0:
                for i in range (len(Chatcommunicate.runningCommands)):
                    if Chatcommunicate.runningCommands [i]["thread"].is_alive() != True:
                        del Chatcommunicate.runningCommands [i]
        except TypeError:
            pass
    
        if shouldShutdown == True or shouldReboot == True:
            TrackBots.saveBotList()
            QuietRooms.saveQuietRoomList ()
            break
        
        if len (TrackBots.botsList) != botListLen:
            botListLen = len (TrackBots.botsList)
            TrackBots.saveBotList()

        if len (QuietRooms.quietRooms) != quietRoomLen:
            quietRoomLen = len (QuietRooms.quietRooms)
            QuietRooms.saveQuietRoomList()
    
        #Check if a bot is dead
        for each_bot in TrackBots.botsList:
            if TrackBots.isBotAlive (each_bot ["user_id"]) == False and each_bot ["status"] == "alive":
                for each_room in each_bot ["rooms"]:
                    postMessage (ceExt.getRoomFromID (each_room), "@" + each_bot ["name"] + " alive")
                currentTime = time.time()
                while (time.time() - currentTime < 30):
                    if TrackBots.isBotAlive (each_bot ["user_id"]) == True:
                        break

                if TrackBots.isBotAlive (each_bot ["user_id"]) == False:
                    for each_room in each_bot ["rooms"]:
                        postMessage(ceExt.getRoomFromID (each_room), Utilities.startLink + " " + each_bot ["name"] + " is dead (" + each_bot ["to_ping"] + ").")
                            
                    each_bot ["status"] = "dead"

        time.sleep (1)

    for each_room in rooms:
        each_room.leave()
