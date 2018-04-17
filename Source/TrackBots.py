#
# TrackBots.py
# Thunder
#
# Created by Ashish Ahuja on 17th April 2018.
# Licensed under WTFPL (http://www.wtfpl.net/).
#

import BotpySE as bp
import time
import threading as thr

class Chatbot:
    def __init__(self, room, name, chat_id, owner_name, wait_time, command_to_run):
        self._room = room
        self._name = name
        self._chat_id = chat_id
        self._owner_name = owner_name
        self._wait_time = wait_time
        self._command_to_run = command_to_run

        self._message_posted = True
        self.alive = False
        self.dead_at = time.time()

    def _post_command(self):
        self._room.send_message(self._command_to_run)
        time.sleep(60)

    def update(self):
        eligible_users = [x for x in self._room._users if x.id == self._chat_id]
        if len(eligible_users) == 0:
            self.alive = False
            return
        user = eligible_users[0]
        
        if (time.time() - user.last_message) > self._wait_time and self.alive:
            self.alive = False
            self._post_command()
            self.update()
            return

        if (time.time() - user.last_message) < self._wait_time and not self.alive:
            self._message_posted = False
            self.alive = True

        if not self.alive and not self._message_posted:
            self._room.send_message(self.name + " is dead @" + self._owner_name.replace(" ", ""))
            self._message_posted = True
