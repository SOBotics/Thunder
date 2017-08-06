import chatexchange
import Utilities
import Chatcommunicate

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
        quiet_rooms.append(QuietRoom(each_dict["room_id"], each_dict["interval"]))

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
