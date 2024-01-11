import pytz
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.local import utc, multiple


class Local:
    def __init__(self):
        self._date = []
        self._final = []
        self._get = []
        self.i = -1

    def button(self) -> InlineKeyboardMarkup:
        for index, date in enumerate(utc):
            self._check(index, utc, [date, date], 4)
            self.i += 1
        print(self.i)
        self.i = -1
        results = InlineKeyboardMarkup(self._final)
        self._final = []
        return results

    def get(self, user: str):
        if user not in multiple:
            return None
        self._get_final(user)
        return InlineKeyboardMarkup(self._final)

    def _get_final(self, user: str):
        self._get_loop(user)
        for index, data in enumerate(self._get):
            self._check(index, self._get, data, 5)
            pass
        return self

    def _get_loop(self, user: str):
        for i in pytz.all_timezones:
            self._get_loop_check(i, user)

    def _get_loop_check(self, data: str, user: str):
        if data.split('/')[0] == user:
            show = data.replace(data.split('/')[0] + "/", '')
            self._get.append([show, data])

    def _check(self, index, first: list, date: list[str, str], line: int):
        self._date.append(InlineKeyboardButton(date[0], callback_data=date[1]))
        if (index + 1) % line == 0:
            self._final.append(self._date)
            self._date = []
        if len(first) - 1 == index and self._date:
            self._final.append(self._date)
            self._date = []
        return self
