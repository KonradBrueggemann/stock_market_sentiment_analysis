from dataframes.dataframe_generator import DataFrame


def main(q, after, before):
    df = DataFrame(q, after, before)
    print(df.dataframe)
    df.save_to_csv()


if __name__ == "__main__":
    query = input("Input Stock Ticker: ")
    start = input("Start Date: ")
    end = input("End Date: ")
    main(query, start, end)
