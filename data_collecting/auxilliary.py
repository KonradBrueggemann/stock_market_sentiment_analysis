import datetime
import time


def unix_timestamp(date):
    chops = date.split("-")
    date = datetime.date(int(chops[2]), int(chops[1]), int(chops[0]))
    return str(int(time.mktime(date.timetuple())))
