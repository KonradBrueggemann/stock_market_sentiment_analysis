import requests


class RedditComments:
    def __init__(self, query, after, before):
        self.query = query
        self.after = after
        self.before = before
        self.url = f"https://api.pushshift.io/reddit/search/comment/" \
                   f"?q={self.query}" \
                   f"&after={self.after}" \
                   f"&before={self.before}" \
                   f"&sort=desc" \
                   f"&size=1000"
        self.data = requests.get(self.url)
        self.reddit = self.data.json()["data"]

    def print_data(self):
        for pleb in self.reddit:
            print(pleb["body"])

    def return_data(self):
        comments = []
        for n, pleb in enumerate(self.reddit):
            comment = pleb["body"]
            comments.append(comment)
            print(f"Comment {n+1}:\n{comment}\n-------")
        return comments

