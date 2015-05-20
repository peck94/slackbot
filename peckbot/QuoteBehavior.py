import urllib2

class QuoteBehavior(object):
    def __init__(self):
        self.name = "Quotes"

    def execute(self, bot, match, channel):
        categories = 'joel_on_software+paul_graham+prog_style+codehappy'
        if match is None:
            match = categories
        req = urllib2.urlopen('http://www.iheartquotes.com/api/v1/random?source={0}'.format(match))
        data = req.read()

        bot.send_msg(data, channel)