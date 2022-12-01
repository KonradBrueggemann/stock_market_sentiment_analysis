from stocktwits_collector.collector import Collector
from dataframes.data_collecting.auxilliary import twit_format


class Stocktwits:
    def __init__(self, query, start):
        self.query = query
        self.start = twit_format(start)
        self.twits = self.get_tweets()

    def get_tweets(self):
        twits = Collector()
        messages = twits.get_history({'symbols': [self.query], 'start': self.start})  # messages have a lot of attrs
        comments = [message["body"] for message in messages]   # so we extract only the body (text content)
        return comments
