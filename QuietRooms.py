import chatexchange
import Utilities
import Chatcommunicate

quietRooms = list()

def getQuietRoomByID (roomID):
    for each_room in quietRooms:
        if each_room ["room_id"] == roomID:
            return each_room

    return None

def addQuietRoom (roomID, interval=120):
    if isRoomQuiet (roomID) == True:
        return
    
    room = Utilities.client.get_room(roomID)
    room.join()
    room.watch_polling (Chatcommunicate.handleMessage, interval)

    Utilities.rooms.append (room)

    quietRooms.append ({"room_id": roomID, "interval": interval})

def deleteQuietRoom (roomID):
    if isRoomQuiet (roomID) == False:
        return

    for each_room in Utilities.rooms:
        if each_room.id == roomID:
            each_room.leave()
            Utilities.rooms.remove (each_room)
            break

    quietRoom = getQuietRoomByID(roomID)
    quietRooms.remove (quietRoom)

def isRoomQuiet (roomID):
    for each_room in quietRooms:
        if each_room ["room_id"] == roomID:
            return True

    return False

def saveQuietRoomList ():
    Utilities.saveToPickle ("quiet_rooms.pickle", quietRooms)

def loadQuietRoomList ():
    return Utilities.loadFromPickle ("quiet_rooms.pickle")

