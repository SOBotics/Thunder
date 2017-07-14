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
import time

Utilities.startTime = time.time()

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

#This will work only if you are running the bot with 'nocrash.sh'.
if BackgroundTasks.shouldReboot == True:
    os.exit (2)

client.logout()

