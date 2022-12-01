import datetime
import time


def unix_timestamp(date):
    """
    helper method to convert a date from D-M-Y format to unix timestamp using datetime and time
    data param has to be in string format. e.g. "01-12-2022"
    """
    chops = date.split("-")
    date = datetime.date(int(chops[2]), int(chops[1]), int(chops[0]))
    return str(int(time.mktime(date.timetuple())))


def twit_format(date):
    chops = date.split("-")
    year = chops[2]
    month = chops[1]
    day = chops[0]
    new_date = f"{year}-{month}-{day}T00:00:00Z"
    return new_date
