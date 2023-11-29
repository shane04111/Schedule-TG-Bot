import re
from datetime import datetime, timezone, timedelta


def time_datetime():
    """
    :return: 當前時間(datetime格式)
    """
    return datetime.now()


def time_date():
    """
    :return: 當前時間(date格式)
    """
    return datetime.now().date()


def time_year():
    """
    :return: 當前年份
    """
    return datetime.now().year


def time_month():
    """
    :return: 當前月份
    """
    return datetime.now().month


def time_day():
    """
    :return: 當前日期
    """
    return datetime.now().day


def utcTime(zone: str = "+08:00"):
    zone_match = re.match(r'([+-])(\d+):(\d+)', zone)
    sign = zone_match.group(1)
    hour = zone_match.group(2)
    minute = zone_match.group(3)
    utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    user_time = utc.astimezone(timezone(timedelta(hours=sign + hour, minutes=sign + minute)))


def myTime():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    now_time = now.time()
    date = now.date()
    return Time(now, year, month, day, hour, minute, second, now_time, date)


class Time:
    def __init__(self, now, year, month, day, hour, minute, second, nowTime, date):
        self.now = now
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.nowTime = nowTime
        self.date = date
