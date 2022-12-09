import basc_py4chan
import datetime


class Py4chan:
    def __init__(self, query, date):
        self.query = query
        self.date = date
        self.all_posts = self.get_posts("/biz/")
        self.relevant = self.filter_relevant_posts()

    def get_posts(self, b):
        board = basc_py4chan.Board(b)
        all_thread_ids = board.get_all_thread_ids()
        posts = []

        for t in all_thread_ids:
            thread = board.get_thread(t)
            try:
                for reply in thread.replies:
                    posts.append(reply)
            except AttributeError:
                continue
        return posts

    def filter_relevant_posts(self):
        comments = []
        for post in self.all_posts:
            if self.query in post.text_comment and post.datetime.strftime("%d-%m-%Y") == self.date:
                comments.append(post.text_comment)
        return comments


if __name__ == "__main__":
    for stock in ["AMZN", "META", "NFLX", "NVDA", "QQQ", "ARK", "MSFT"]:
        chan = Py4chan(stock, "07-12-2022")
        print(stock + ":")
        print(chan.relevant)
