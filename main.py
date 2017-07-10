#!/usr/bin/python
import getpass
import logging
import os
import threading
import sys
import BackgroundTasks

import Utilities
import Chatcommunicate
from Utilities import client
import chatexchange

if 'ThunderEmail' in os.environ:
    email = os.environ['ThunderEmail']
else:
    email = input("Email: ")

if 'ThunderPass' in os.environ:
    password = os.environ['ThunderPass']
else:
    password = getpass.getpass("Password: ")

print ("Logging in...")

client = chatexchange.Client(Utilities.host, email, password)
myself = client.get_me()

backgroundThread = threading.Thread (target=BackgroundTasks.scheduleBackgroundTasks, args=(client, Utilities.roomIDs), kwargs={})

backgroundThread.start()
backgroundThread.join()

#TODO: This triggers a permission denied error (OS X)
if BackgroundTasks.shouldReboot == True:
    os.execv(__file__, sys.argv)

client.logout()

