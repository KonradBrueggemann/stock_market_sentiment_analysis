import nltk.sentiment.vader as sev
import numpy as np


class SentimentAnalysis:
    def __init__(self, query):
        self.query = query
        self.comments = self.get_comments()
        self.sia = sev.SentimentIntensityAnalyzer()

    def return_polarity_score(self, chunk):
        return self.sia.polarity_scores(chunk)['compound']

    def get_comments(self):
        return  # get comments from reddit class

    def get_mean_score(self):
        total = [self.return_polarity_score(comment) for comment in self.comments]
        return np.mean(total)
