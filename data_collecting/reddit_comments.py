import requests

from auxilliary import unix_timestamp


class RedditComments:
    def __init__(self, query, after, before):
        self.query = query
        self.after = after
        self.before = before
        self.url = f"https://api.pushshift.io/reddit/search/comment/" \
                   f"?q={self.query}" \
                   f"&after={self.after}" \
                   f"&before={self.before}" \
                   f"&sort=desc"
        self.data = requests.get(self.url)
        self.reddit = self.data.json()["data"]

    def return_data(self):
        for pleb in self.reddit:
            print(pleb["body"])


q = "NFLX"
after = "01-11-2022"
after = unix_timestamp(after)
before = "01-12-2022"
before = unix_timestamp(before)

if __name__ == "__main__":
    reddit = RedditComments(q, after, before)
    reddit.return_data()
