import chatexchange
import os
import sys
import BackgroundTasks
import Chatcommunicate

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

commandList = {
    "alive": commandAlive,
    "reboot": commandReboot,
    "kill": commandKill,
    "shutdown": commandShutdown,
    "running commands": commandListRunningCommands,
    "rc": commandListRunningCommands,
}
