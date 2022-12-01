from data_collecting.auxilliary import unix_timestamp
from data_collecting.reddit_comments import RedditComments
from text_processing.sentiment_analysis import SentimentAnalysis


class ScoreChart:
    def __init__(self, query, after, before):
        self.query = query
        self.after = unix_timestamp(after)   # takes date in D-M-Y format and converts it to unix timestamp
        self.before = unix_timestamp(before)
        self.comments = self.get_comments()
        self.sentiment = self.get_polarity_score()

    def get_comments(self):
        """
        uses RedditComments class to make a request to the pushshift.io reddit archive
        a list of comments will be returned
        """
        reddit = RedditComments(self.query, self.after, self.before)
        return reddit.return_data()

    def get_polarity_score(self):
        """ calls SentimentAnalysis class to get the mean sentiment polarity score for the comment list """
        SA = SentimentAnalysis(self.comments)
        return SA.get_mean_score()

