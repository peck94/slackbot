class DocBehavior(object):
    def __init__(self):
        self.name = 'Doxx'

    def execute(self, bot, match, channel):
        msg = 'Yes, this is peckbot\n'
        msg += 'Available behaviors:\n'
        for resp in bot.responses:
            regex, behavior = resp
            msg += '{0}: /{1}/\n'.format(behavior.name, regex)
        msg += 'That is all.'
        bot.send_msg(msg, channel)