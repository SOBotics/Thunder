#!/usr/bin/python
import chatexchange
import os
import sys
import BackgroundTasks
import Chatcommunicate
import TrackBots
import time
import Utilities
from tabulate import tabulate
import re
import datetime
from subprocess import call
import datetime
from chatexchangeExtension import postMessage
from chatexchangeExtension import postReply
import QuietRooms

def commandAlive (message, args):
    secsAlive = time.time () - Utilities.startTime
    uptime = divmod (secsAlive, 60)
    secs = int(uptime [1])
    hrUptime = divmod (uptime [0], 60)
    mins = int(hrUptime [1])
    hrs = int(hrUptime [0])
    
    postReply (message, Utilities.botLink + " running since " + str (hrs) + " hours, " + str (mins) + " minutes and " + str (secs) + " seconds.")

def commandHelp (message, args):
    postReply (message, "I'm " + Utilities.botLink + ", a status monitoring bot for SOBotics.")

def commandReboot (message, args):
    postReply(message, "Rebooting...")
    BackgroundTasks.shouldReboot = True

def commandShutdown (message, args):
    postReply(message, "Shutting down...")
    BackgroundTasks.shouldShutdown = True

def commandKill (message, args):
    os._exit(1)

def commandListRunningCommands (message, args):
    commandList = list()
    for each_command in Chatcommunicate.runningCommands:
        commandList.append ([each_command["user"], each_command["command"]])
    
    table = tabulate (commandList, headers=["User", "Command"], tablefmt="orgtbl")

    postMessage (message.room, "    " + re.sub ('\n', '\n    ', table))

def commandTrackBot (message, args):
    newBot = {"name": "unknown", "user_id": -1, "to_ping": "unknown", "time_to_wait": -1, "last_message_time": time.time(), "rooms": [], "status": "alive"}
    
    for each_arg in args:
        if each_arg.startswith ("name="):
            newBot ["name"] = each_arg.replace ("name=", "")
        elif each_arg.startswith("userid="):
            newBot ["user_id"] = int(each_arg.replace ("userid=", ""))
        elif each_arg.startswith("userID="):
            newBot ["user_id"] = int(each_arg.replace ("userID=", ""))
        elif each_arg.startswith("user_id="):
            newBot ["user_id"] = int(each_arg.replace ("user_id=", ""))
        elif each_arg.startswith("to_ping="):
            newBot ["to_ping"] = each_arg.replace ("to_ping=", "")
        elif each_arg.startswith("time_to_wait="):
            newBot ["time_to_wait"] = int (each_arg.replace ("time_to_wait=", ""))
        elif each_arg.startswith ("rooms="):
            stripped_arg = each_arg.replace ("rooms=")
            newBot ["rooms"] = stripped_arg.split (",")

    if len (newBot["rooms"]) == 0:
        newBot["rooms"] = [message.room.id]

    if (newBot["name"] == "unknown") or (newBot ["user_id"] == -1) or (newBot ["to_ping"] == "unknown") or (newBot ["time_to_wait"] == -1):
        postReply (message, "Please provide adequate arguments: `name`, `user_id`, `to_ping`, `time_to_wait` and optionally `rooms`.")
    else:
        TrackBots.botsList.append (newBot)
        postReply (message, "Bot '" + newBot ["name"] + "' has been added to the bot watch list.")

#TODO: Make this take args starting with 'userid='
def commandUntrackBot (message, args):
    TrackBots.deleteBot (int (args [0]))
    postReply(message, "Bot with userID '" + args [0] + "' has been deleted.")

def commandUpdateBot (message, args):
    userID = -1
    if args [0].startswith("userid="):
        userID = int (args[0].replace ("userid=", ""))
    elif args [0].startswith("user_id="):
        userID = int (args[0].replace ("user_id=", ""))
    elif args [0].startswith("userID="):
        userID = int (args[0].replace ("userID=", ""))

    if userID == -1:
        postReply (message, "Please give the user id as the first argument (`userid=<userid>`).")

    botIndex = TrackBots.getBotIndexByID (userID)

    if botIndex == -1:
        postReply (message, "The userID you have given does not exist in the bot database.")
        return

    del args [0]

    for each_arg in args:
        if each_arg.startswith ("time_to_wait="):
            TrackBots.botsList [botIndex]["time_to_wait"] = int (each_arg.replace ("time_to_wait=", ""))
        elif each_arg.startswith ("to_ping="):
                TrackBots.botsList [botIndex]["to_ping"] = each_arg.replace ("to_ping=", "")

    postReply (message, "The bot has been updated.")

def commandListBots (message, args):
    botList = list()
    for each_bot in TrackBots.botsList:
        botList.append ([each_bot["name"], each_bot ["status"], str(datetime.timedelta(seconds=(time.time() - each_bot["last_message_time"]))) + " ago. "])
    
    table = tabulate (botList, headers=["Bot", "Status", "Last known alive time"], tablefmt="orgtbl")

    #The regex puts four spaces after every newline so that the table is formatted as code.
    print (repr("    " + re.sub ('\n', '\n    ', table)))
    postMessage (message.room, "    " + re.sub ('\n', '\n    ', table))

def commandUpdateCode (message, args):
    call (["git", "pull", "origin", "master"])
    BackgroundTasks.shouldReboot = True
    postReply (message, "Updating...")

def commandAddQuietRoom (message, args):
    roomID = 0
    interval = 120

    for each_arg in args:
        if each_arg.startswith("roomid="):
            roomID = int (each_arg.replace ("roomid=", ""))
        elif each_arg.startswith("interval="):
            interval = int (each_arg.replace ("interval=", ""))

    if roomID == 0:
        postReply (message, "Please provide a `roomid=` and optionally an `interval=`.")
        return

    QuietRooms.addQuietRoom (roomID, interval)

    postReply (message, "Quiet room with id '" + str (roomID) + "' has been added.")

def commandDeleteQuietRoom (message, args):
    roomID = 0
    if args [0].startswith ("roomid="):
        roomID = int (args [0].replace ("roomid=", ""))
    else:
        postReply (message, "Please provide a `roomid=`.")
        return

    QuietRooms.deleteQuietRoom (roomID)

    postReply (message, "Quiet room with id '" + str (roomID) + "' has been deleted.")

def commandListRooms (message, args):
    roomList = list()
    for each_room in Utilities.rooms:
        roomList.append ([each_room.name, each_room.id, "Normal" if QuietRooms.isRoomQuiet (each_room.id) != True else "Quiet"])

    table = tabulate (roomList, headers=["Name", "Room ID", "Type"], tablefmt="orgtbl")
    print (repr (table))
    postMessage (message.room, "    " + re.sub ('\n', '\n    ', table))

commandList = {
    "alive": commandAlive,
    "reboot": commandReboot,
    "kill": commandKill,
    "stop": commandShutdown,
    "running commands": commandListRunningCommands,
    "rc": commandListRunningCommands,
    "track * * * * ...": commandTrackBot,
    "untrack *": commandUntrackBot,
    "update * * ...": commandUpdateBot,
    "listbots": commandListBots,
    "pull": commandUpdateCode,
    "help": commandHelp,
    "status": commandAlive,
    "uptime": commandAlive,
    "commands": commandHelp,
    "addquiet *": commandAddQuietRoom,
    "deletequiet *": commandDeleteQuietRoom,
    "listrooms": commandListRooms,
}
