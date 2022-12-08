from pmaw import PushshiftAPI
from dataframes.data_collecting.auxilliary import unix_timestamp


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
        """
        for the sake of the quality of the comments, as well as runtime purposes, only wsb, r/trading and r/stocks
        will be fetched
        from each sub a maximum of 1000 comments within the given time frame will be stored
        """
        subs = ["wallstreetbets", "trading", "stocks"]
        commentlst = []
        for sub in subs:
            comments = self.api.search_comments(q=self.query,
                                                before=self.before,
                                                after=self.after,
                                                limit=1000,
                                                subreddit=sub)
            commentlst.extend([comment for comment in comments])
        return commentlst


if __name__ == "__main__":
    reddit = RedditComments("tsla", unix_timestamp("01-12-2022"), unix_timestamp("02-12-2022"))
    print(reddit.comments)
