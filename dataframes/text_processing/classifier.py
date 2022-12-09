import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import *
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class Classifier:
    def __init__(self):
        """
        Initializes the Classifier object
        df: the training set
        vectorizer, tfidfconverter: instances needed to train the model
        classifier is trained using the initialize_model method
        """
        pd.set_option('max_colwidth', 1000)
        self.df = pd.read_csv("resources/twitter_2013_labelled_tweets.csv")
        self.vectorizer = CountVectorizer(max_features=2000, min_df=0.0001, max_df=0.9)
        self.tfidfconverter = TfidfTransformer()
        self.classifier, self.X, self.y = self.initialize_model()

    def initialize_model(self):
        """
        initializes and trains a Naive Bayes model to classify tweet sentiment as positive, negative or neutral
        :return:
        the model as well as the X and y datapoints which will be passed to the evaluation method
        """
        X, y = self.df["text"], self.df["sentiment"]

        X = self.vectorizer.fit_transform(X).toarray()
        X = self.tfidfconverter.fit_transform(X).toarray()

        model = MultinomialNB()
        model.fit(X, y)

        return model, X, y

    def test_model(self):
        """
        splits the datapoints into training sets and test sets
        since we already trained the model we only need the test sets
        on the test set we perform predictions
        :return:
        classification report of the accuracy of the predictions
        """
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        y_pred = self.classifier.predict(X_test)
        return classification_report(y_test, y_pred)

    def classify(self, tweet):
        """ takes sample tweet and predicts its sentiment """
        sample = self.vectorizer.transform([tweet])
        return self.classifier.predict(sample)[0]   # return obj is list with prediction so we take 0th element


if __name__ == "__main__":
    c = Classifier()
    print(c.test_model())
    while True:
        print(c.classify(str(input("Tweet: "))))
