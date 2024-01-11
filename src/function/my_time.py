import re
from datetime import datetime, timezone, timedelta


def utcTime(zone: str = "+08:00"):
    zone_match = re.match(r'([+-])(\d+):(\d+)', zone)
    sign = 1 if zone_match.group(1) == '+' else -1
    hour = zone_match.group(2)
    minute = zone_match.group(3)
    utc = datetime.utcnow().replace(tzinfo=timezone.utc)
    user_time = utc.astimezone(timezone(timedelta(hours=sign * hour, minutes=sign * minute)))


def myTime():
    now = datetime.now()
    return Time(now)


class Time:
    def __init__(self, now):
        self.now = now
        pass

    def year(self):
        return self.now.year

    def month(self):
        return self.now.month

    def day(self):
        return self.now.day

    def hour(self):
        return self.now.hour

    def minute(self):
        return self.now.minute

    def second(self):
        return self.now.second

    def nowTime(self):
        return self.now.time()

    def date(self):
        return self.now.date()

    def week(self):
        return self.now.weekday()

    def check_time(self, year: int, month: int):
        """
        檢查時間是否為當月
        :param year:
        :param month:
        :return:
        """
        if year == self.year() and month == self.month():
            return True
        return False
