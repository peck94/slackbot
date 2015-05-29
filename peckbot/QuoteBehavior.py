import urllib2
import HTMLParser

class QuoteBehavior(object):
    def __init__(self):
        self.name = "Quotes"
        self.parser = HTMLParser.HTMLParser()

    def execute(self, bot, match, event):
        channel = event['channel']
        categories = 'joel_on_software+paul_graham+prog_style+codehappy'
        if match == '':
            match = categories
        try:
            req = urllib2.urlopen('http://www.iheartquotes.com/api/v1/random?source={0}'.format(match))
            data = self.parser.unescape(req.read())
        except Exception as e:
            data = '{0}\nCategories: {1}'.format(e, match)

        bot.send_msg(data, channel)