from dataframes.dataframe_generator import DataFrame
from threading import Thread
from multiprocessing import Process

import time


def main(q, after, before):
    df = DataFrame(q, after, before)
    print(df.dataframe)
    df.save_to_csv()


if __name__ == "__main__":
    stocks = ["NFLX", "TSLA"]
    start = "01-11-2022"
    end = "07-11-2022"

    threads = [Process(target=main, args=(stock, start, end)) for stock in stocks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Done.")
