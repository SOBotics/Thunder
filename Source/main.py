#
# main.py
# Thunder
#
# Created by Ashish Ahuja on 17th April 2018.
# Licensed under WTFPL (http://www.wtfpl.net).
#

import BotpySE as bp
import chatexchange as ce

import TrackBots as tb
from commands import all_commands 

import os
import subprocess
import getpass

class Thunder:
    def __init__(self, name, email, password, rooms):
        self._bot_header = '[ [Thunder](https://github.com/SOBotics/Thunder) ]'
        
        self.bot = bp.Bot(name, all_commands, rooms, [], "stackoverflow.com", email, password)

        try:
            with open(self.bot._storage_prefix + 'redunda_key.txt', 'r') as file_handle:
                key = file_handle.readlines()[0].rstrip('\n')
            self.bot.set_redunda_key(key)
        except IOError as ioerr:
            print(str(ioerr))
            print("Redunda key not found; starting without Redunda integration!")

        self.bot.redunda_init(bot_version=self._get_current_hash())
        self.bot.set_redunda_default_callbacks()
        self.bot.set_redunda_status(True)

        self.bot.set_startup_message(self._bot_header + " started on " + self.bot._location + ".")
        self.bot.set_standby_message(self._bot_header + " running on " + self.bot._location + " shifting to standby.")
        self.bot.set_failover_message(self._bot_header + " running on " + self.bot._location + " received failover.")

        self.bot.start()
        self.bot.add_privilege_type(1, "owner")
        self.bot.set_room_owner_privs_max()

        self._track_bots = tb.TrackBots(self.bot)
        self.bot._command_manager._track_bots = self._track_bots

    def _get_current_hash(self):
        return subprocess.run(['git', 'log', '-n', '1', '--pretty=format:"%H"'], stdout=subprocess.PIPE).stdout.decode('utf-8')[1:8]

if __name__ == "__main__":
    if 'ThunderEmail' in os.environ:
        email = os.environ['ThunderEmail']
    else:
        email = input("Email: ")

    if 'ThunderPass' in os.environ:
        password = os.environ['ThunderPass']
    else:
        password = getpass.getpass("Password: ")

    Thunder("Thunder", email, password, rooms=[111347])
