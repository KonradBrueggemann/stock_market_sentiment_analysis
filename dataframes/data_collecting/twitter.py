from dataframes.data_collecting.twitter_config import *
from dataframes.data_collecting.auxilliary import tweet_to_dmy


class Twitter:
    def __init__(self, query, date):
        self.query = query
        self.date = date
        self.tweets = self.get_query_tweets()

    def get_query_tweets(self):
        """
        searches for n amount of tweets containing the query
        :return:
        list of tweet objects
        """
        fetched_tweets = api.search_tweets(q=f"{self.query}",
                                           lang="en",
                                           result_type="popular",
                                           tweet_mode='extended',
                                           )
        return [tweet.full_text for tweet in fetched_tweets if tweet_to_dmy(str(tweet.created_at)) == self.date]


if __name__ == "__main__":
    tweets = Twitter("NFLX", "06-12-2022")
    for tweet in tweets.tweets:
        print(tweet)
