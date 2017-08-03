import chatexchange
import Utilities
import Chatcommunicate

"""
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
"""

quiet_rooms = list()

def add_quiet_room(room_id, join=True, interval=120):
    quiet_room = QuietRoom(room_id, interval)
    quiet_rooms.append (quiet_room)

    if join:
        quiet_room.watch_room()

def get_quiet_room(room_id):
    for each_room in quiet_rooms:
        if each_room.room_id == room_id:
            return each_room

    #TODO: Throw an error.
    return None   

def delete_quiet_room(room_id, leave=True):
    for each_room in quiet_rooms:
        if each_room.room_id == room_id:
            if leave:
                each_room.leave_room()
            quiet_rooms.remove (each_room)

def is_room_quiet(room_id):
    for each_room in quiet_rooms:
        if each_room.room_id == room_id:
            return True

    return False

def save_room_list():
    dict_list = list()

    for each_room in quiet_rooms:
        dict_list.append({"room_id": each_room.room_id, "interval": each_room.interval})

    Utilities.saveToPickle("quietroomlist.pickle", dict_list)

def load_room_list():
    dict_list = Utilities.loadFromPickle("quietroomlist.pickle")

    for each_dict in dict_list:
        quiet_rooms.append(QuietRoom(dict_list["room_id"], dict_list["interval"]

class QuietRoom:
    def __init__(self, room_id, interval):
        self.room_id = room_id
        self.interval = interval

    def watch_room(self):
        room = Utilities.client.get_room(self.room_id)
        room.join()
        room.watch_polling(Chatcommunicate.handleMessage, self.interval)
    
        Utilities.rooms.append(room)

    def rejoin_room(self):
        self.leave_room()
        self.watch_room()

    def leave_room(self):
        for each_room in Utilities.rooms:
            if each_room.id == self.room_id:
                each_room.leave()
                Utilities.rooms.remove(each_room)
