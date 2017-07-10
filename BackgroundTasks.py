import chatexchange
import threading
import Chatcommunicate
import time
from Utilities import rooms

shouldShutdown = False
shouldReboot = False

def listenForMessages (client, roomIDs):
    for each_id in roomIDs:
        rooms.append (client.get_room (each_id))

    for each_room in rooms:
        each_room.join()
        print ("Joined room " + str(each_room.id) + ".")
    
        each_room.watch (Chatcommunicate.handleMessage)


def scheduleBackgroundTasks (client, roomIDs):
    #Listen for input
    inputListener = threading.Thread (target=listenForMessages, args=(client, roomIDs), kwargs={})

    inputListener.start()

    while (1):
        try:
            #Remove commands which have completed.
            if len (Chatcommunicate.runningCommands) > 0:
                for i in range (len(Chatcommunicate.runningCommands)):
                    if Chatcommunicate.runningCommands [i]["thread"].is_alive() == False:
                        del Chatcommunicate.runningCommands [i]
        except TypeError:
            pass
    
        if shouldShutdown == True or shouldReboot == True:
            break

        time.sleep (1)

    for each_room in rooms:
        each_room.leave()
