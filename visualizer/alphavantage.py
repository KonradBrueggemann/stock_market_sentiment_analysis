import pandas
import pandas as pd
from alpha_vantage.timeseries import TimeSeries


class AlphaVantage:
    def __init__(self, symbol, api_key):
        self.symbol = symbol
        self.api_key = api_key

    def retrieve_historical_data(self):
        ts = TimeSeries(self.api_key, output_format='pandas')
        data, meta = ts.get_daily_adjusted(self.symbol, outputsize='full')
        columns = ['open', 'high', 'low', 'close', 'adjusted close', 'volume', 'dividend', 'split cf']
        data.columns = columns
        data.reset_index(inplace=True)
        df = data.rename(columns={'index': 'date'})
        print(df.head())
        return df
