import json
import urllib2

class TriviaBehavior(object):
    def __init__(self):
        self.name = 'Trivia'
        self.current_trivia = None
        self.scores = {}

    def execute(self, bot, match, event):
        words = match.split(' ')
        channel = event['channel']
        user_id = event['user']
        user = json.loads(bot.client.api_call('users.info', user=user_id))['user']['name']

        if words[0] == '' or words[0] == 'new':
            req = urllib2.urlopen('http://jservice.io/api/random')
            self.current_trivia = json.loads(req.read())[0]
            bot.send_msg('[{0}] {1}\n({2} points)'.format(self.current_trivia['category']['title'],
                                                          self.current_trivia['question'],
                                                          self.current_trivia['value']), channel)

            print('[TRIVIA] Current trivia:')
            print(self.current_trivia)
        elif words[0] == 'repeat':
            bot.send_msg('[{0}] {1}\n({2} points)'.format(self.current_trivia['category']['title'],
                                                          self.current_trivia['question'],
                                                          self.current_trivia['value']), channel)
        elif words[0] == 'answer':
            if self.current_trivia is None:
                bot.send_msg('No question.', channel)
            elif self.current_trivia['answer'] == ' '.join(words[1:]):
                value = self.current_trivia['value']
                bot.send_msg('Correct! +{0} points.'.format(value), channel)
                self.current_trivia = None

                if not user in self.scores:
                    self.scores[user] = value
                else:
                    self.scores[user] += value
            else:
                bot.send_msg('Nope.', channel)
        elif words[0] == 'scores':
            output = 'Leaderboard:\n'
            for u in self.scores:
                output += '{0}: {1}\n'.format(u, self.scores[u])
            bot.send_msg(output, channel)