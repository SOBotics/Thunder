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

    QuietRooms.load_room_list()

    for each_room in QuietRooms.quiet_rooms:
        print ("Joined quiet room " + str (each_room.room_id) + ".")
        each_room.watch_room()

def scheduleBackgroundTasks (client, roomIDs):
    global shouldReboot
    
    #Listen for input
    inputListener = threading.Thread (target=listenForMessages, args=(client, roomIDs), kwargs={})

    inputListener.start()
    
    botListLen = len (TrackBots.bots_list)
    quietRoomLen = len (QuietRooms.quiet_rooms)
    lastSaveTime = time.time()
    
    #Load the list of bots from the pickle
    TrackBots.load_bot_list()

    while (1):
        try:
            #Remove commands which have completed.
            if len (Chatcommunicate.runningCommands) > 0:
                for each_command in Chatcommunicate.runningCommands:
                    if not each_command["thread"].is_alive:
                        Chatcommunicate.runningCommands.remove(each_command)
        except TypeError:
            pass
    
        if Utilities.Redunda:
            Utilities.Redunda.sendStatusPing()
    
        if shouldShutdown == True or shouldReboot == True:
            TrackBots.save_bot_list()
            QuietRooms.save_room_list ()
            break
        
        if len (TrackBots.bots_list) != botListLen:
            botListLen = len (TrackBots.bots_list)
            TrackBots.save_bot_list()

        if len (QuietRooms.quiet_rooms) != quietRoomLen:
            quietRoomLen = len (QuietRooms.quiet_rooms)
            QuietRooms.save_room_list()
        
        #Save files every 60 seconds.
        if time.time() - lastSaveTime >= 60:
            lastSaveTime = time.time()
            TrackBots.save_bot_list()
            QuietRooms.save_room_list()
    
        #Check if a bot is dead
        for each_bot in TrackBots.bots_list:
            if not each_bot.is_bot_alive() and each_bot.alive:
                timeBeforeMessage = time.time()
                
                for each_room in each_bot.rooms:
                    postMessage (ceExt.getRoomFromID (each_room), "@" + each_bot.name + " alive")
                
                #Check if the bot is not listening to messages.
                while time.time() - timeBeforeMessage < 10:
                    if (time.time () - Utilities.lastMessageTime) < (time.time () - timeBeforeMessage):
                        break
                
                if time.time () - Utilities.lastMessageTime > 10:
                    #The bot is not listening to messages anymore; post a message indicating that and then auto-reboot.
                    ceExt.postMessageInRooms (Utilities.rooms, Utilities.startLink + "I am not listening to chat messages (cc @ashish). Auto-reboot in progress...")
                    print ("I am not listening to chat messages. Auto-reboot in progress...")
                    shouldReboot = True
                else:
                    currentTime = time.time()
                    while (time.time() - currentTime < 30):
                        if each_bot.is_bot_alive():
                            break

                    if not each_bot.is_bot_alive():
                        for each_room in each_bot.rooms:
                            postMessage(ceExt.getRoomFromID (each_room), Utilities.startLink + " " + each_bot.name + " is dead (" + "@ashish" + ").")
                            
                        each_bot.alive = False

        time.sleep (1)

    for each_room in rooms:
        each_room.leave()
