import matplotlib.pyplot as plt
import pandas as pd


class Stock:
    def __init__(self, data, symbol, start_date, end_date):
        self.data = data
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date

    def plot_data_frame(self):
        print(self.data.head())
        start_date = pd.to_datetime(self.start_date)
        end_date = pd.to_datetime(self.end_date)
        self.data[self.data['date'].between(start_date, end_date)].plot(x='date', y='close', kind='line')
        plt.title("%s TIME SERIES DAILY ADJUSTED" % self.symbol)
        plt.show()
