import nltk.sentiment.vader as sev
import numpy as np


class SentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments   # these will be passed in list format from the main class
        self.sia = sev.SentimentIntensityAnalyzer()

    def return_polarity_score(self, chunk):
        return self.sia.polarity_scores(chunk)['compound']   # compound key contains the actual score

    def get_mean_score(self):
        total = [self.return_polarity_score(comment) for comment in self.comments]
        return float(np.round(np.mean(total), 5))   # get mean score for list of comments
