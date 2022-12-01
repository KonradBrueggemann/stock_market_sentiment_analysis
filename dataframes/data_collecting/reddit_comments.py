import requests


class RedditComments:
    def __init__(self, query, after, before):
        self.query = query   # stock ticker
        self.after = after   # start of time period
        self.before = before   # end of time period
        self.url = f"https://api.pushshift.io/reddit/search/comment/" \
                   f"?q={self.query}" \
                   f"&after={self.after}" \
                   f"&before={self.before}" \
                   f"&sort=desc" \
                   f"&size=1000"
        self.data = requests.get(self.url)   # gets the data from pushshift.io archive
        self.reddit = self.data.json()["data"]

    def print_data(self):
        for pleb in self.reddit:
            print(pleb["body"])

    def return_data(self):
        """ from a dataset containing pushshift reddit comment objects,
        only the actual comment text will be stored in a list """
        return [comment["body"] for comment in self.reddit]

