# NLTK for traditional approach
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk.sentiment.vader as sev

# for removing punctuations from the tokens
from string import punctuation

# math
import numpy as np
import pandas as pd

# machine learning based approach
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

import torch


class SentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments   # these will be passed in list format from the main class
        self.volume = self.get_post_volume()
        self.senti_table = pd.read_csv("resources/Loughran-McDonald_MasterDictionary_1993-2021.csv")
        self.sia = sev.SentimentIntensityAnalyzer()
        self.model_name = f"cardiffnlp/twitter-roberta-base-sentiment"
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(self.device)

    def return_polarity_score(self, token, type):
        if type == "roberta":
            encoded_text = self.tokenizer(token, return_tensors="pt")
            output = self.model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            scores_dict = {
                "neg": scores[0],
                "neu": scores[1],
                "pos": scores[2]
            }
            return scores_dict["pos"]

        elif type == "nltk":
            return self.sia.polarity_scores(token)["compound"]

    def tokenize(self, comment):
        stop = stopwords.words()
        tokens = word_tokenize(comment)
        tokens = [token for token in tokens if token not in stop and token not in punctuation]
        return tokens

    def sentenize(self, comment):
        return nltk.sent_tokenize(comment)

    def get_pos_tag(self, token):
        tup = nltk.pos_tag([token])
        return tup[0][1]

    def _get_mean_score(self):
        total = []
        for comment in self.comments:
            sentences = self.sentenize(comment)
            for sentence in sentences:
                total.append(self.return_polarity_score(sentence, type="nltk"))
        return total

    def get_mean_score(self):
        total = self._get_mean_score()
        result = float(np.round(np.mean(total), 5))
        return result if self.volume > 0 else 0   # get mean score for list of comments, if no comments return 0

    def get_post_volume(self):
        return len(self.comments)
