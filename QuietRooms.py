import chatexchange
import Utilities
import Chatcommunicate

quietRooms = list()

def addQuietRoom (roomID):
    if isRoomQuiet (roomID) == True:
        return
    
    room = Utilities.client.get_room(roomID)
    room.join()
    room.watch (Chatcommunicate.handleMessage)

    Utilities.rooms.append (room)

    quietRooms.append (roomID)

def deleteQuietRoom (roomID):
    if isRoomQuiet (roomID) == False:
        return

    for each_room in Utilities.rooms:
        if each_room.id == roomID:
            each_room.leave()
            Utilities.rooms.remove (each_room)
            break

    quietRooms.remove (roomID)

def isRoomQuiet (roomID):
    for each_room in quietRooms:
        if each_room == roomID:
            return True

    return False

def saveQuietRoomList ():
    Utilities.saveToPickle ("quiet_rooms.pickle", quietRooms)

def loadQuietRoomList ():
    return Utilities.loadFromPickle ("quiet_rooms.pickle")

