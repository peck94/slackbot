#!python
from PeckBot import PeckBot

# params
token = 'xoxb-4959650590-ljQjJFuJowucBjJuDgxi0kV7'
timeout = 3

# init bot
peckbot = PeckBot(token, timeout)
if peckbot.connect():
    peckbot.run()
else:
    print('[ERROR] Could not connect to Slack RTM')
