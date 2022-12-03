import requests
import pandas as pd

from pmaw import PushshiftAPI


class RedditComments:
    def __init__(self, query, after, before):
        self.query = query   # stock ticker
        self.after = int(after)   # start of time period
        self.before = int(before)   # end of time period
        self.api = PushshiftAPI()
        self.reddit = self._get_comments()  # gets the data from pushshift.io archive
        self.comments = self.return_data()   # extracts the actual texts from the data

    def return_data(self):
        """ from a dataset containing pushshift reddit comment objects,
        only the actual comment text will be stored in a list """
        return [comment["body"] for comment in self.reddit]

    def _get_comments(self):
        comments = self.api.search_comments(q=self.query, before=self.before, after=self.after, limit=1000)
        commentlst = [comment for comment in comments]
        return commentlst

