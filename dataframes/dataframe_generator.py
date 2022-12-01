from dataframes.scores_for_source import ScoreChart
from datetime import date, timedelta

import pandas as pd
import time


class DataFrame:
    def __init__(self, query, start_date, end_date, sources):
        self.query = query
        self.start = start_date
        self.end = end_date
        self.sources = sources
        self.dates = self.list_of_dates()   # list of all dates within timeframe (start-end), in D-M-Y format
        self.dataframe = self.convert_to_pandas_df()

    def list_of_dates(self):
        """ generates a list of dates between two dates """

        start_chops = self.start.split("-")
        month = int(start_chops[1])   # the input is a string like "12-05-2022"
        year = int(start_chops[2])    # so the first slice is the day and so on
        day = int(start_chops[0])
        sdate = date(year, month, day)

        end_chops = self.end.split("-")
        month = int(end_chops[1])
        year = int(end_chops[2])
        day = int(end_chops[0])
        edate = date(year, month, day)

        timestamps = pd.date_range(sdate, edate-timedelta(days=1), freq='d').to_list()
        date_list = [str(stamp.date().strftime("%d-%m-%Y")) for stamp in timestamps]
        print(date_list)

        return date_list

    def get_sentiment_score(self, start, end):
        score = ScoreChart(self.query, start, end, self.sources)
        return score.get_polarity_score()

    @staticmethod
    def calc_day_after(sdate):
        """
        simple method to increase the day in a D-M-Y date string by 1
        doesnt account for months (yet)
        """
        date_chops = str(sdate).split("-")
        month = int(date_chops[1])
        year = int(date_chops[2])
        day = int(date_chops[0])
        current_date = date(year, month, day)
        next_day = current_date + timedelta(days=1)
        return next_day.strftime("%d-%m-%Y")

    def run_through_datelist(self):
        """ iterates through the date list to get the SP score for each day """
        date_score_dict = {}
        for start_date in self.dates:
            end_date = self.calc_day_after(start_date)   # to get the comments of day X, do X-M-Y to (X+1)-M-Y
            date_score_dict[start_date] = self.get_sentiment_score(start_date, end_date)
            time.sleep(1.5)   # this makes sure the pushshift.io API is ready for the next request
        return date_score_dict

    def convert_to_pandas_df(self):
        """ simple method to turn the dictionary generated by the run_through_datelist() function into a dataframe """
        data = self.run_through_datelist()   # returns dict
        date_col = data.keys()    # get dates
        value_col = data.values()   # get SP scores
        frame = {"Date": date_col, "Sentiment Score": value_col}
        return pd.DataFrame.from_dict(frame)

    def save_to_csv(self):
        file = self.dataframe
        file.to_csv(f'output/{self.query}.csv', index=False, sep=";", decimal=",")
