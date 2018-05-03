#
# bots.py
# Thunder
#
# Created by Ashish Ahuja on 3rd May 2018.
# Licensed under WTFPL (http://www.wtfpl.net).
#

import BotpySE as bp
import tabulate as tb
import re

class CommandPrivilegeUser(bp.CommandPrivilegeUser):
    def privileges(self):
        return 1

class CommandUnprivilegeUser(bp.CommandUnprivilegeUser):
    def privileges(self):
        return 1

class CommandStop(bp.CommandStop):
    def privileges(self):
        return 1

class CommandReboot(bp.CommandReboot):
    def privileges(self):
        return 1

class CommandListChatbots(bp.Command):
    @staticmethod
    def usage():
        return ["listbots", "botstatus", "bots", "list"]

    def run(self):
        botList = list()
        for bot in self.command_manager._track_bots._chatbots:
            botList.append([bot._name, bot.status()])
        table = tb.tabulate(botList, headers=["Name", "Status"], tablefmt="orgtbl")

        self.post("    " + re.sub('\n', '\n    ', table))

all_commands = [bp.CommandAlive, bp.CommandListRunningCommands, CommandPrivilegeUser, CommandStop, CommandUnprivilegeUser, bp.CommandAmiprivileged, bp.CommandListPrivilegedUsers, CommandReboot, CommandListChatbots]
