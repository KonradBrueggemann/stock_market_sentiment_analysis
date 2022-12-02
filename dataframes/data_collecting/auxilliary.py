import datetime
import time
from datetime import date, timedelta

def unix_timestamp(date):
    """
    helper method to convert a date from D-M-Y format to unix timestamp using datetime and time
    data param has to be in string format. e.g. "01-12-2022"
    """
    chops = date.split("-")
    date = datetime.date(int(chops[2]), int(chops[1]), int(chops[0]))
    return str(int(time.mktime(date.timetuple())))


def twit_format(date):
    """
    helper method that converts date from D-M-Y format to Y-M-D and adds T00:00:00Z
    """
    chops = date.split("-")
    year = chops[2]
    month = chops[1]
    day = chops[0]
    new_date = f"{year}-{month}-{day}T00:00:00Z"
    return new_date


def vantage_date(date):
    start_chops = date.split("-")
    month = int(start_chops[1])  # the input is a string like "12-05-2022"
    year = int(start_chops[2])  # so the first slice is the day and so on
    day = int(start_chops[0])
    if day < 10:
        day = f"0{day}"
    return f"{year}-{month}-{day}"


def calc_day_after(sdate):
    """
    simple method to increase the day in a D-M-Y date string by 1
    """
    date_chops = str(sdate).split("-")
    month = int(date_chops[1])
    year = int(date_chops[2])
    day = int(date_chops[0])
    current_date = date(year, month, day)
    next_day = current_date + timedelta(days=1)
    return next_day.strftime("%d-%m-%Y")


def calc_day_before(sdate):
    """
    simple method to decrease the day in a Y-M-D date string by 1
    """
    date_chops = str(sdate).split("-")
    month = int(date_chops[1])
    year = int(date_chops[0])
    day = int(date_chops[2])
    print(day, month, year)
    current_date = date(year, month, day)
    previous_day = current_date - timedelta(days=1)
    return previous_day.strftime("%d-%m-%Y")
