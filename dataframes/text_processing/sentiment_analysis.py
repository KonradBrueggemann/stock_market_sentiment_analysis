import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from string import punctuation

import nltk.sentiment.vader as sev
import numpy as np
import pandas as pd


class SentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments   # these will be passed in list format from the main class
        self.volume = self.get_post_volume()
        self.senti_table = pd.read_csv("resources/Loughran-McDonald_MasterDictionary_1993-2021.csv")

    def return_polarity_score(self, token):
        # get index of row where word column value is the token
        index = self.senti_table.index[self.senti_table['Word'] == token.upper()].to_list()
        if not index:   # if there is no such value, return 0 (neutral score)
            return 0
        else:
            index = index[0]  # index is a list with one element
        negative = self.senti_table.at[index, "Negative"]
        positive = self.senti_table.at[index, "Positive"]
        if negative == 0 and positive != 0:
            return 1
        elif negative != 0 and positive == 0:
            return -1
        elif negative == 0 and positive == 0:
            return 0

    def tokenize(self, comment):
        stop = stopwords.words()
        tokens = word_tokenize(comment)
        tokens = [token for token in tokens if token not in stop and token not in punctuation]
        return tokens

    def get_post_tag(self, token):
        tup = nltk.pos_tag([token])
        return tup[0][1]

    def get_mean_score(self):
        total = []
        for comment in self.comments:
            tokens = self.tokenize(comment)
            for token in tokens:
                total.append(self.return_polarity_score(token))
        return float(np.round(np.mean(total), 5))   # get mean score for list of comments

    def get_post_volume(self):
        return len(self.comments)
