from scores_for_source import ScoreChart
from data_collecting.auxilliary import unix_timestamp

import pandas as pd


class DataFrame:
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start = start_date
        self.end = end_date
        self.dates = self.list_of_dates()

    def list_of_dates(self):
        date_list = []

        start_chops = self.start.split("-")
        month = int(start_chops[1])
        year = int(start_chops[2])
        start = int(start_chops[0])

        end_chops = self.end.split("-")
        end = int(end_chops[0])

        for i in range(start, end + 1):
            date = f"{i}-{month}-{year}"
            date_list.append(date)

        return date_list

    def get_sentiment_score(self, start, end):
        score = ScoreChart(self.query, start, end)
        return score.get_polarity_score()

    @staticmethod
    def calc_day_after(date):
        date_chops = date.split("-")
        month = int(date_chops[1])
        year = int(date_chops[2])
        day = int(date_chops[0])
        res = f"{day+1}-{month}-{year}"
        print(res)
        return res

    def run_through_datelist(self):
        date_score_dict = {}
        for start_date in self.dates:
            end_date = self.calc_day_after(start_date)
            print(start_date + " " + end_date)
            date_score_dict[start_date] = self.get_sentiment_score(start_date, end_date)
        return date_score_dict

    def convert_to_pandas_df(self):
        data = self.run_through_datelist()
        date_col = data.keys()
        value_col = data.values()
        frame = {"Date": date_col, "Sentiment Score": value_col}
        return pd.DataFrame.from_dict(frame)


q = "NFLX"
after = "01-01-2022"
before = "03-01-2022"

if __name__ == "__main__":
    df = DataFrame(q, after, before)
    print(df.list_of_dates())
    print(df.run_through_datelist())
    print(df.convert_to_pandas_df())
