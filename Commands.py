#!/usr/bin/python
import chatexchange
import os
import sys
import BackgroundTasks
import Chatcommunicate
import TrackBots
import time
from tabulate import tabulate
import re
import datetime
from subprocess import call

def commandAlive (message, args):
    message.message.reply ("yes!")

def commandReboot (message, args):
    message.message.reply ("Rebooting...")
    BackgroundTasks.shouldReboot = True

def commandShutdown (message, args):
    message.message.reply ("Shutting down...")
    BackgroundTasks.shouldShutdown = True

def commandKill (message, args):
    os._exit(1)

#TODO: Fix the output of this command (the message does not get formatted as code)
def commandListRunningCommands (message, args):
    if len (Chatcommunicate.runningCommands) == 0:
        message.message.reply ("There are no running commands, so there is something wrong. cc @ashish")
        return

    commandsMessage = "         User     |    Command    \n"

    for each_command in Chatcommunicate.runningCommands:
        userSpaces = 14 - len (each_command ["user"])
        commandSpaces = 15 - len (each_command ["command"])

        commandsMessage += "    "

        if userSpaces >= 4:
            commandsMessage += "  " + each_command["user"]
            laterSpaces = userSpaces - 2

            for i in range (laterSpaces):
                commandsMessage += " "

            commandsMessage += "\n"
        else:
            commandsMessage += each_command["user"]

            for i in range (userSpaces):
                commandsMessage += " "

            commandsMessage += "\n"

        commandsMessage += "|   " + each_command ["command"] + "\n"

    message.room.send_message (commandsMessage)

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
        message.message.reply ("Please provide adequate arguments: `name`, `user_id`, `to_ping`, `time_to_wait` and optionally `rooms`.")
    else:
        TrackBots.botsList.append (newBot)
        message.message.reply ("Bot '" + newBot ["name"] + "' has been added to the bot watch list.")

def commandUntrackBot (message, args):
    TrackBots.deleteBot (int (args [0]))
    message.message.reply ("Bot with userID '" + args [0] + "' has been deleted.")

def commandUpdateBot (message, args):
    userID = -1
    if args [0].startswith("userid="):
        userID = int (args[0].replace ("userid=", ""))
    elif args [0].startswith("user_id="):
        userID = int (args[0].replace ("user_id=", ""))
    elif args [0].startswith("userID="):
        userID = int (args[0].replace ("userID=", ""))

    if userID == -1:
        message.message.reply ("Please give the user id as the first argument (`userid=<userid>`).")

    botIndex = TrackBots.getBotIndexByID (userID)

    if botIndex == -1:
        message.message.reply ("The userID you have given does not exist in the bot database.")
        return

    del args [0]

    for each_arg in args:
        if each_arg.startswith ("time_to_wait="):
            TrackBots.botsList [botIndex]["time_to_wait"] = int (each_arg.replace ("time_to_wait=", ""))
        elif each_arg.startswith ("to_ping="):
                TrackBots.botsList [botIndex]["to_ping"] = each_arg.replace ("to_ping=", "")

def commandListBots (message, args):
    botList = list()
    for each_bot in TrackBots.botsList:
        botList.append ([each_bot["name"], each_bot ["status"], str(datetime.timedelta(seconds=(time.time - each_bot["last_message_time"]))) + " ago. "])
    
    table = tabulate (botList, headers=["Bot", "Status", "Last known alive time"],tablefmt="orgtbl")

    #The regex puts four spaces after every newline so that the table is formatted as code.
    message.room.send_message ("    " + re.sub ('\n', '\n    ', table))

def commandUpdateCode (message, args):
    call (["git", "pull", "origin", "master"])
    BackgroundTasks.shouldReboot = True
    message.message.reply ("Updating...")

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
}
