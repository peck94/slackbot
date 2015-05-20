from slackclient import SlackClient
import time
import re
from RedditBehavior import RedditBehavior
from DocBehavior import DocBehavior
from CleverBotBehavior import CleverBotBehavior
from QuoteBehavior import QuoteBehavior

class PeckBot(object):
    def __init__(self, token, timeout):
        self.token = token
        self.client = SlackClient(token)
        self.timeout = timeout
        self.userid = 'U04U7K4HC'
        self.responses = [
            ('r/([a-zA-Z0-9]+)', RedditBehavior()),
            ('peckbot: ?(.*)$', CleverBotBehavior()),
            ('^peckdoc$', DocBehavior()),
            ('peckbot quote ?(.*)$', QuoteBehavior())
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
                    if 'user' in event and event['user'] != self.userid:
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