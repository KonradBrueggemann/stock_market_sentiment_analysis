from dataframes.data_collecting.twitter_config import *
from dataframes.data_collecting.auxilliary import tweet_to_dmy

import pandas as pd
import random


class Twitter:
    def __init__(self, query, date):
        """
        uses tweepy API to search for tweets containing a keyword on a specific date
        the text content of the tweets will be accumulated in a list
        :param query: the stock ticker query which will be received
        :param date: the date from which tweets will be searched for
        """
        self.query = query
        self.date = date
        self.tweets = self.get_query_tweets()
        # these are for the dataset creation to train the classifier model
        self.stock_symbols = pd.read_csv("resources/top_stock_tickers.csv")["Ticker"].values
        self.df = pd.DataFrame(columns=["Tweet", "Sentiment"])

    def get_query_tweets(self):
        """
        searches for tweets containing the query
        :return:
        list of tweet texts
        """
        fetched_tweets = api.search_tweets(q=f"${self.query}",   # on twitter you use $AAPL when talking about AAPL
                                           lang="en",
                                           result_type="popular",
                                           tweet_mode='extended',
                                           )
        return [tweet.full_text for tweet in fetched_tweets if tweet_to_dmy(str(tweet.created_at)) == self.date]

    def make_csv(self, stock_list):
        """
        performs a tweepy search for each stock in the stock list and appends the results to a dataframe
        :param stock_list: list of stock tickers that are deemed important/representative
        :return: csv file will be stored in tweets/
        """
        api.wait_on_rate_limit = True
        api.wait_on_rate_limit_notify = True
        for stock in stock_list:
            tweets = api.search_tweets(q=stock,
                                       lang="en",
                                       result_type="popular",
                                       tweet_mode='extended')
            comments = [tweet.full_text for tweet in tweets]
            for comment in comments:
                row = [comment, "neutral"]
                self.df.loc[len(self.df)] = row

        self.df.to_csv("tweets/tweets_dataset_12_2022.csv", index=True, sep=",", encoding="UTF-8")


if __name__ == "__main__":
    tweets = Twitter("NFLX", "06-12-2022")
    tweets.make_csv([symbol for symbol in tweets.stock_symbols])
