#!/usr/bin/python
import chatexchange
import Utilities
import QuietRooms

def getRoomFromID (roomID):
    for each_room in Utilities.rooms:
        if each_room.id == roomID:
            return each_room

    return each_room

def isUserRO (roomID, userID):
    room = getRoomFromID (roomID)

    for each_owner in room.owners:
        if each_owner.id == userID:
            return True

    return False

def postMessageInRooms (rooms, message):
    for each_room in rooms:
        postMessage (each_room, message)

def postMessage (room, message):
    if QuietRooms.is_room_quiet(room.id) == True:
        return

    room.send_message (message, length_check=False)

def postReply (message, text):
    if QuietRooms.is_room_quiet(message.room.id) == True:
        return

    message.message.reply (text)
