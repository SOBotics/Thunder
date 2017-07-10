import chatexchange
import os
import sys
import BackgroundTasks

def commandAlive (message, args):
    message.message.reply ("yes!")

def commandReboot (message):
    message.message.reply ("Rebooting...")

    if __name__ == '__main__':
        print ("uh")
        os.execv(__file__, sys.argv)
        print ("huh")
    else:
        print (__name__)

def commandShutdown (message, args):
    message.message.reply ("Shutting down...")
    BackgroundTasks.shouldShutdown = True

def commandKill (message, args):
    os._exit(1)

commandList = {
    "alive": commandAlive,
    "reboot": commandReboot,
    "kill": commandKill,
    "shutdown": commandShutdown,
#"kill": commandKill,
}
