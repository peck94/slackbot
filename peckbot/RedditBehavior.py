import praw

class RedditBehavior(object):
    def __init__(self):
        self.praw = praw.Reddit(user_agent='PeckySlack')
        self.name = 'Reddit'

    def execute(self, bot, subreddit, event):
        channel = event['channel']
        submissions = self.praw.get_subreddit(subreddit).get_hot(limit=5)
        for submission in submissions:
            author = submission.author
            title = submission.title
            url = submission.permalink

            bot.send_msg("/u/{0}: {1} [{2}]".format(author, title, url), channel)