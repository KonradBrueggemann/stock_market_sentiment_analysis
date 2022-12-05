from stocktwits_collector.collector import Collector
from dataframes.data_collecting.auxilliary import twit_format


class Stocktwits:
    def __init__(self, query, start, end):
        self.query = query
        self.start = twit_format(start)
        self.end = twit_format(end)
        self.twits = self.get_tweets()

    def get_tweets(self):
        twits = Collector()
        messages = twits.get_history({'symbols': [self.query], 'start': self.start}) # messages have a lot of attrs
        comments = [message["body"] for message in messages if message["created_at"] == str(self.start).partition("T")[0]] # so we extract only the body (text content)
        return comments


if __name__ == "__main__":
    twits = Stocktwits("NFLX", "03-12-2022", "04-12-2022")
    print(twits.twits[:3])
