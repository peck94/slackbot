from cleverbot import Cleverbot

class CleverBotBehavior(object):
    def __init__(self):
        self.cleverbot = Cleverbot()
        self.name = 'Cleverbot'

    def execute(self, bot, msg, channel):
        bot.send_msg(self.cleverbot.ask(msg), channel)