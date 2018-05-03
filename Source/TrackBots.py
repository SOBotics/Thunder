#
# TrackBots.py
# Thunder
#
# Created by Ashish Ahuja on 17th April 2018.
# Licensed under WTFPL (http://www.wtfpl.net).
#

import BotpySE as bp
import time
import threading as thr

import bots

class Chatbot:
    def __init__(self, room, name, chat_id, owner_name, wait_time, command_to_run):
        self._room = room
        self._name = name
        self._chat_id = chat_id
        self._owner_name = owner_name
        self._wait_time = wait_time
        self._command_to_run = command_to_run

        self._message_posted = False
        self.alive = True

    def _post_command(self):
        self._room.send_message(self._command_to_run)
        time.sleep(60)

    def status(self):
        return "Alive" if self.alive else "Dead"

    def update(self):
        print("[Chatbot#update] Status check running for bot " + self._name + ".")
        eligible_users = [x for x in self._room._users if x.id == self._chat_id]
        if len(eligible_users) == 0:
            self.alive = False
            return
        user = eligible_users[0]
        user.scrape_profile()

        if user.last_message > self._wait_time and self.alive:
            print("[ChatBot#update] Bot " + self._name + " has not posted a message since more than " + str(self._wait_time) + " seconds.")
            self.alive = False
            self._post_command()
            self.update()
            return

        if user.last_message < self._wait_time and not self.alive:
            print("[ChatBot#update] Bot " + self._name + " is now alive once again!")
            self._message_posted = False
            self.alive = True

        if not self.alive and not self._message_posted:
            print("[ChatBot#update] Bot " + self._name + " is dead.")
            self._room.send_message(self._name + " is dead @" + self._owner_name.replace(" ", ""))
            self._message_posted = True

class TrackBots:
    def __init__(self, botpy):
        self._bot = botpy
        self._chatbots = list()

        for bot in bots.bots:
            room = next((x for x in self._bot._rooms if x.id == bot['room']), None)
            
            if room is not None:
                self._chatbots.append(Chatbot(room, bot['name'], bot['chat_id'], bot['owner_name'], bot['wait_time'], bot['command_to_run']))
                print("[TrackBots#init] Adding bot " + bot['name'] + " to chatbot tracking.") 
            else:
                print("[TrackBots#init] Error: room with id '" + str(bot.room) + "' does not exist in Bot class.")

        for chatbot in self._chatbots:
            self._bot._background_task_manager.add_background_task(bp.BackgroundTask(chatbot.update, interval=90))
        self._bot._background_task_manager.restart_tasks()  
