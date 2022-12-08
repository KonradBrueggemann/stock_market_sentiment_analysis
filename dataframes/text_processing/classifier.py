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
        self.df = pd.read_csv("resources/twitter_2013_labelled_tweets.csv")
        self.vectorizer = CountVectorizer(max_features=1500, min_df=0.0009, max_df=0.9)
        self.tfidfconverter = TfidfTransformer()
        self.model = self.initialize_model()
        self.classifier = self.model[0]
        self.X = self.model[1]
        self.y = self.model[2]

    def initialize_model(self):
        X, y = self.df["text"], self.df["sentiment"]

        X = self.vectorizer.fit_transform(X).toarray()
        X = self.tfidfconverter.fit_transform(X).toarray()

        model = MultinomialNB()
        model.fit(X, y)

        return model, X, y

    def test_model(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        y_pred = self.classifier.predict(X_test)
        return classification_report(y_test, y_pred)

    def classify(self, tweet):
        sample = self.vectorizer.transform([tweet])
        return self.classifier.predict(sample)[0]


if __name__ == "__main__":
    c = Classifier()
    print(c.test_model())
    while True:
        print(c.classify(str(input("Tweet: "))))
