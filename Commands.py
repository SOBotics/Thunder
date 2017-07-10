import chatexchange
import os
import sys
import BackgroundTasks

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

#def commandListRunningCommands (message, args):
    #TODO: Complete this command

commandList = {
    "alive": commandAlive,
    "reboot": commandReboot,
    "kill": commandKill,
    "shutdown": commandShutdown,
#"kill": commandKill,
}
