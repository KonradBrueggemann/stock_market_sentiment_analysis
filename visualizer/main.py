from alphavantage import AlphaVantage
from stock_chart import Stock

if __name__ == '__main__':
    start = '2022-07-15'
    end = '2022-09-16'
    while True:
        try:
            symbol = input("ticker symbol: ").upper()
            a = AlphaVantage(symbol, 'A4KHMHCIPDDDD8WI')
            df = a.retrieve_historical_data()
        except ValueError:
            print('try again')
        else:
            break

    s = Stock(df, symbol, start, end)
    s.plot_data_frame()
    df.to_csv('output2.csv')