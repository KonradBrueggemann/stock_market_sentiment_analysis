from stocktwits_collector.collector import Collector
from dataframes.data_collecting.auxilliary import twit_format


class Stocktwits:
    def __init__(self, query, start):
        self.query = query
        self.start = twit_format(start)
        self.twits = self.get_tweets()

    def get_tweets(self):
        twits = Collector()
        messages = twits.get_history({'symbols': [self.query], 'start': self.start})
        comments = [message["body"] for message in messages]
        return comments


if __name__ == "__main__":
    pyt = Stocktwits("AMZN", '29-11-2022')
    twits = pyt.twits
    print(twits)
