import nltk.sentiment.vader as sev
import numpy as np


class SentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments
        self.sia = sev.SentimentIntensityAnalyzer()

    def return_polarity_score(self, chunk):
        return self.sia.polarity_scores(chunk)['compound']

    def get_mean_score(self):
        total = [self.return_polarity_score(comment) for comment in self.comments]
        return np.mean(total)
