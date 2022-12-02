from dataframes.dataframe_generator import DataFrame
from multiprocessing import Process


def main(q, after, before, sources):
    df = DataFrame(q, after, before, sources)
    print(df.dataframe)
    df.save_to_csv()


if __name__ == "__main__":
    stocks = ["NFLX", "AMZN", "NVDA", "NVTA", "TSLA"]
    start = "01-11-2022"
    end = "01-12-2022"
    sources = ["reddit"]

    threads = [Process(target=main, args=(stock, start, end, sources)) for stock in stocks]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("Done.")
