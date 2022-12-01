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
