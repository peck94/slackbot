import pickle
import random
import re

class NonsensBehavior(object):
    def __init__(self):
        self.words = {} # w -> ([(v_1, f_1), ..., (v_n, f_n)], t)
        self.max_size = 4
        self.load()

    def save(self):
        file = open('nonsens.dat', 'w')
        pickle.dump(self.words, file)
        file.close()

    def load(self):
        try:
            file = open('nonsens.dat', 'r')
            self.words = pickle.load(file)
            file.close()
        except:
            pass

    def filter(self, word):
        word = word.lower()
        word = word.replace('\n', ' ')
        word = word.replace('\r', ' ')
        word = re.sub(r'[^a-z0-9\.\?\!\; \']', '', word)
        word = re.sub(r' +', ' ', word)
        return word

class NonsensTrainingBehavior(NonsensBehavior):
    def __init__(self):
        super(NonsensTrainingBehavior, self).__init__()
        self.name = 'NonsensTraining'

    def execute(self, bot, match, event):
        words = self.filter(match).split(' ')
        for k in range(1, self.max_size+1):
            print('Training size: {0}/{1}'.format(k, self.max_size))
            for i in range(0, len(words)-k):
                current = self.filter(words[i])
                next = ' '.join(words[i+1:i+k+1])

                if current in self.words:
                    found = False
                    pairs, total = self.words[current]
                    for j in range(0, len(pairs)):
                        word, freq = pairs[j]
                        if word == next:
                            pairs[j] = (word, freq+1)
                            self.words[current] = (pairs, total+1)
                            found = True
                            break

                    if not found:
                        pairs.append((next, 1))
                        self.words[current] = (pairs, total+1)
                else:
                    self.words[current] = ([], 0)
        self.save()

    def train(self, filename):
        file = open(filename, 'r')
        self.execute(None, file.read(), None)
        file.close()

class NonsensSpewingBehavior(NonsensBehavior):
    def __init__(self):
        super(NonsensSpewingBehavior, self).__init__()
        self.name = 'NonsensSpew'
        self.max_len = 50

    def execute(self, bot, match, event):
        words = self.filter(match).split(' ')
        word = words[random.randrange(0, len(words))]
        count = 0

        if word in self.words:
            output = word
            next = self.spew(word)
            while next is not None and count < self.max_len:
                output = '{0} {1}'.format(output, next)
                next = self.spew(next.split(' ')[-1])
                count += 1
            bot.send_msg(output, event['channel'])

    def spew(self, word):
        if word not in self.words:
            return None

        pairs, total = self.words[word]
        if total == 0:
            return None

        for w, f in pairs:
            if random.random() <= float(f)/float(total):
                return w

        w, _ = pairs[random.randrange(0, len(pairs))]
        return w