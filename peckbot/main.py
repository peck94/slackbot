#!python
from slackclient import SlackClient
import praw
import time
import re
from cleverbot import Cleverbot

class CleverBotBehavior(object):
    def __init__(self):
        self.cleverbot = Cleverbot()
        self.name = 'Cleverbot'

    def execute(self, bot, msg, channel):
        bot.send_msg(self.cleverbot.ask(msg), channel)

class RedditBehavior(object):
    def __init__(self):
        self.praw = praw.Reddit(user_agent='PeckySlack')
        self.name = 'Reddit'

    def execute(self, bot, subreddit, channel):
        submissions = self.praw.get_subreddit(subreddit).get_hot(limit=5)
        for submission in submissions:
            author = submission.author
            title = submission.title
            url = submission.permalink

            bot.send_msg("/u/{0}: {1} [{2}]".format(author, title, url), channel)

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

class PeckBot(object):
    def __init__(self, token, timeout):
        self.token = token
        self.client = SlackClient(token)
        self.timeout = timeout
        self.userid = 'U04U7K4HC'
        self.responses = [
            ('r/([a-zA-Z0-9]+)', RedditBehavior()),
            ('peckbot: ?(.*)$', CleverBotBehavior()),
            ('^peckdoc$', DocBehavior())
        ]

    def connect(self):
        return self.client.rtm_connect()

    def send_msg(self, msg, channel):
        self.client.rtm_send_message(channel, msg)
        self.pause()

    def pause(self):
        time.sleep(self.timeout)

    def run(self):
        print('[INFO] PeckBot is running')
        while True:
            events = self.client.rtm_read()
            for event in events:
                if 'type' in event and event['type'] == 'message':
                    if event['user'] != self.userid:
                        self.respond(event['text'], event['channel'])
            self.pause()

    def respond(self, text, channel):
        for resp in self.responses:
            regex, behavior = resp
            matches = re.findall(regex, text)
            for match in matches:
                print('[INFO] Triggered {0} on {1}'.format(behavior.name, channel))
                try:
                    behavior.execute(self, match, channel)
                except Exception as e:
                    print('[ERROR] {0} failed: {1}'.format(behavior.name, e))

# params
token = 'xoxb-4959650590-ljQjJFuJowucBjJuDgxi0kV7'
timeout = 3

# init bot
peckbot = PeckBot(token, timeout)
if peckbot.connect():
    peckbot.run()
else:
    print('[ERROR] Could not connect to Slack RTM')
