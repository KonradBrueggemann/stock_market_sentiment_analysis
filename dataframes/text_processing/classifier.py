import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import *
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

from nltk.corpus import stopwords


class Classifier:
    def __init__(self):
        pd.set_option('max_colwidth', 1000)
        self.df = pd.read_csv("twitter_2013_labelled_tweets.csv")
        self.vectorizer = CountVectorizer(max_features=2000, min_df=5, max_df=0.7, stop_words=stopwords.words())
        self.tfidfconverter = TfidfTransformer()
        self.model = self.initialize_model()

    def initialize_model(self):
        X, y = self.df["text"], self.df["sentiment"]

        X = self.vectorizer.fit_transform(X).toarray()
        X = self.tfidfconverter.fit_transform(X).toarray()

        model = MultinomialNB()
        model.fit(X, y)

        return model

    def classify(self, tweet):
        sample = self.vectorizer.transform([tweet])
        return self.model.predict(sample)[0]


if __name__ == "__main__":
    c = Classifier()
    print(c.classify(str(input("Tweet: "))))
