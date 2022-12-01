from data_collecting.auxilliary import unix_timestamp
from data_collecting.reddit_comments import RedditComments
from text_processing.sentiment_analysis import SentimentAnalysis


class ScoreChart:
    def __init__(self, query, after, before):
        self.query = query
        self.after = unix_timestamp(after)
        self.before = unix_timestamp(before)
        self.comments = self.get_comments()
        self.sentiment = self.get_polarity_score()

    def get_comments(self):
        print(self.query, self.after, self.before)
        reddit = RedditComments(self.query, self.after, self.before)
        return reddit.return_data()

    def get_polarity_score(self):
        SA = SentimentAnalysis(self.comments)
        return SA.get_mean_score()


q = "NFLX"
after = "01-01-2022"
after = unix_timestamp(after)
before = "01-02-2022"
before = unix_timestamp(before)

if __name__ == "__main__":
    scores = ScoreChart(q, after, before)
    print(scores.get_polarity_score())
