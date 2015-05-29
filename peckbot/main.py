#!python
from PeckBot import PeckBot

# params
token = 'xoxb-5074595580-1cacXuoE2kiwt9NHmMADsKO9'
timeout = 3

# init bot
peckbot = PeckBot(token, timeout)
if peckbot.connect():
    peckbot.run()
else:
    print('[ERROR] Could not connect to Slack RTM')
