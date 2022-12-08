from dataframes.data_collecting.twitter_config import *
from dataframes.data_collecting.auxilliary import tweet_to_dmy

import pandas as pd
import random


class Twitter:
    def __init__(self, query, date):
        self.query = query
        self.date = date
        self.tweets = self.get_query_tweets()
        self.stock_symbols = pd.read_csv("resources/top_stock_tickers.csv")["Ticker"].values
        self.df = pd.DataFrame(columns=["Tweet", "Sentiment"])

    def get_query_tweets(self):
        """
        searches for n amount of tweets containing the query
        :return:
        list of tweet objects
        """
        fetched_tweets = api.search_tweets(q=f"${self.query}",
                                           lang="en",
                                           result_type="popular",
                                           tweet_mode='extended',
                                           )
        return [tweet.full_text for tweet in fetched_tweets if tweet_to_dmy(str(tweet.created_at)) == self.date]

    def make_csv(self, stock_list):
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
