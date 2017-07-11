#!/usr/bin/python
import chatexchange
import Utilities

def getRoomFromID (roomID):
    for each_room in Utilities.rooms:
        if each_room.id == roomID:
            return each_room

    return None

def isUserRO (roomID, userID):
    room = getRoomFromID (roomID)

    for each_owner in room.owners:
        if each_owner.id == userID:
            return True

    return False
