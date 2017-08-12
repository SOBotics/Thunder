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
import pyRedunda
import time

Utilities.startTime = time.time()

#Check for Redunda key and location
if os.path.isfile(str(os.path.expanduser("~")) + "/redunda_key.txt"):
    with open(str(os.path.expanduser("~")) + "/redunda_key.txt", "r") as redunda_file:
        redunda_key = str(redunda_file.read()).replace(" ", "").replace("\n", "")
    
    Utilities.Redunda = pyRedunda.Redunda (redunda_key, Utilities.files_to_sync, "production")
    Utilities.Redunda.sendStatusPing()
    Utilities.location = Utilities.Redunda.location

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
Utilities.client = client
Utilities.myself = client.get_me()
Utilities.myUserID = Utilities.myself.id

while BackgroundTasks.shouldShutdown or BackgroundTasks.shouldReboot:
    while Utilities.shouldStandby:
        Utilities.Redunda.sendStatusPing()
        time.sleep(45)

    backgroundThread = threading.Thread (target=BackgroundTasks.scheduleBackgroundTasks, args=(client, Utilities.roomIDs), kwargs={})

    backgroundThread.start()
    backgroundThread.join()

#This will work only if you are running the bot with 'nocrash.sh'.
if BackgroundTasks.shouldReboot == True:
    print ("Rebooting...")
    os._exit (2)

client.logout()

