import pandas as pd

from visualizer.alphavantage import AlphaVantage
from visualizer.stock_chart import Stock

from dataframes.data_collecting.auxilliary import vantage_date

import os
from os.path import exists


class Visualizer:
    def __init__(self, start, end, ticker):
        self.start = vantage_date(start)
        self.end = vantage_date(end)
        self.ticker = ticker

    def get_data(self):
        file_name = f'resources/{self.ticker}_price_data.csv'
        if not exists(file_name):
            alpha = AlphaVantage(self.ticker, 'A4KHMHCIPDDDD8WI')
            data = alpha.retrieve_historical_data()
            data.to_csv(file_name)
        else:
            data = pd.read_csv(file_name)
        return data

    def show_data(self):
        data = self.get_data()
        stock = Stock(data, self.ticker, self.start, self.end)
        stock.plot_data_frame()

    def main(self):
        os.makedirs("output", exist_ok=True)
        self.show_data()


if __name__ == '__main__':
    vis = Visualizer("2022-11-11", "2022-11-20", "TSLA")
    vis.main()
