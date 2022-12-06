from dataframes.data_collecting.auxilliary import unix_timestamp, vantage_date, calc_day_before
from dataframes.data_collecting.reddit_comments import RedditComments
from dataframes.data_collecting.stocktwits import Stocktwits
from dataframes.text_processing.sentiment_analysis import SentimentAnalysis
from visualizer.main import Visualizer

import pandas as pd


class ScoreChart:
    def __init__(self, query, after, before, sources):
        self.query = query
        self.start = after   # stocktwits scraper doesnt need the unix timestamp
        self.end = before
        self.after = unix_timestamp(after)   # takes date in D-M-Y format and converts it to unix timestamp
        self.before = unix_timestamp(before)
        self.sources = sources
        self.comments = self.get_comments()
        self.reddit_sentiment = SentimentAnalysis(self.comments["reddit"][:100])
        self.rsent = self.get_polarity_score_reddit()
        self.stocktwits_sentiment = SentimentAnalysis(self.comments["stocktwits"][:100])
        self.tsent = self.get_polarity_score_stocktwits()
        self.AV = Visualizer(after, before, query)

    def get_comments(self):
        """
        uses RedditComments class to make a request to the pushshift.io reddit archive
        a list of comments will be returned
        """
        comments = {}

        if "reddit" in self.sources:
            reddit = RedditComments(self.query, self.after, self.before)
            comments["reddit"] = reddit.comments

        if "stocktwits" in self.sources:
            stocktwits = Stocktwits(self.query, self.start, self.end)
            comments["stocktwits"] = stocktwits.twits

        return comments

    def get_polarity_score_reddit(self):
        """ calls SentimentAnalysis class to get the mean sentiment polarity score for the comment list """
        return self.reddit_sentiment.get_mean_score()

    def get_polarity_score_stocktwits(self):
        """ calls SentimentAnalysis class to get the mean sentiment polarity score for the comment list """
        return self.stocktwits_sentiment.get_mean_score()

    def get_volume(self):
        """ calls SentimentAnalysis class to get the comment volume"""
        vol = 0
        for source in self.sources:
            vol += len(self.comments[source])
        return vol

    def _get_last_business_day(self, data, date):
        if vantage_date(date) in data['date'].values:
            return vantage_date(date)
        else:
            return self._get_last_business_day(data, calc_day_before(date))

    def get_close_price(self):
        data = pd.read_csv(f'resources/{self.query}_price_data.csv')
        date = self._get_last_business_day(data, self.start)
        return data.loc[data['date'] == date, 'close'].item()


