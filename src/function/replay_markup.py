import math
import time
from calendar import Calendar
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.ScheduleModel import SqlModel
from src.function.logger import logger
from src.function.my_time import myTime

sql = SqlModel()


class Button:
    def __init__(self, lang):
        self._lang = lang
        self._button = InlineKeyboardButton
        pass

    def create(self, text: str, callback):
        return self._button(lg.get(text, self._lang), callback_data=callback)


class MarkUp(Button):
    def firstCheck(self) -> InlineKeyboardMarkup:
        tf = InlineKeyboardMarkup([
            [
                self.create("button.text.true", 'text_true'),
                self.create("button.text.save", 'save'),
                self.create("button.text.false", 'cancel')
            ]
        ])
        return tf

    def finalCheck(self) -> InlineKeyboardMarkup:
        check = InlineKeyboardMarkup([
            [
                self.create("button.config.true", 'config_true'),
                self.create("button.config.false", 'config_false')
            ],
            self.back('config_back')
        ])
        return check

    def back(self, data: str):
        bc = [
            self.create('button.back', data),
            self.create('button.cancel', 'cancel')
        ]
        return bc


class DateSelect(Button):
    def __init__(self, lang):
        super().__init__(lang)
        self.cld = Calendar()
        self._final_data = []
        self._data = []
        self._week = ["time.mon", "time.tue", "time.wed", "time.thu", "time.fri", "time.sat", "time.sun"]
        self._week_callback = ["-0week", "-6week", "-5week", "-4week", "-3week", "-2week", "-1week"]
        pass

    @staticmethod
    def tick(func):
        def wrapper(*args, **kwargs):
            t1 = time.time()
            result = func(*args, **kwargs)
            t2 = time.time() - t1
            logger.debug(f'{func.__name__} 花了 {t2} 秒運行')
            return result
        return wrapper

    def final(self):
        return InlineKeyboardMarkup(self._final_data)

    @tick
    def date_pick(self, year: int, month: int, style: int):
        self._year(year, month)
        self._month(year, month)
        self._save_data()
        month_week = self.cld.monthdays2calendar(year, month)
        data = _turn(month_week)
        for _ in range(style):
            self._week.insert(0, self._week.pop())
            self._week_callback.insert(0, self._week_callback.pop())
        for index, date_language in enumerate(self._week):
            self._data.append(self.create(date_language, f"{year}/{month}{self._week_callback[index]}"))
        self._save_data()
        if style:
            self._style_sunday(data, year, month, style)
        else:
            self._style_monday(data, year, month)
        self._data.append(self.create('<', _month_callback(year, month)))
        self._data.append(self.create('>', _month_callback(year, month, True)))
        self._final_data.append(self._data)
        self._final_data.append(MarkUp(self._lang).back('date_chose'))
        return self

    @tick
    def select_month(self, year: int, month: int):
        self._year(year, month, 'month')
        self._save_data()
        self._data.extend([
            self.create(f'time.month.{i}', f'{year}/{i}date-pick') for i in range(1, 7)
        ])
        self._save_data()
        self._data.extend([
            self.create(f'time.month.{i}', f'{year}/{i}date-pick') for i in range(7, 13)
        ])
        self._save_data()
        return self

    @tick
    def select_year(self, year: int, month: int):
        self._month(year, month, 'year')
        self._save_data()
        year_first = year // 10 * 10
        self._data.extend([
            self._button(lg.get('time.year.full', self._lang, year_first + i),
                         callback_data=f'{year_first + i}/{month}date-pick') for i in range(5)
        ])
        self._save_data()
        self._data.extend([
            self._button(lg.get('time.year.full', self._lang, year_first + i),
                         callback_data=f'{year_first + i}/{month}date-pick') for i in range(5, 10)
        ])
        self._save_data()
        self._data.append(self.create('<', f'{year_first - 10}/{month}year'))
        self._data.append(self._button(lg.get('time.year.select', self._lang, year_first, year_first + 9),
                                       callback_data=f'{year_first}/{month}all-year'))
        self._data.append(self.create('>', f'{year_first + 10}/{month}year'))
        self._save_data()
        return self

    @tick
    def year_all(self, year: int, month: int):
        for i in range(year - 70, year + 80, 10):
            self._year_all_loop(i, year, month)
        return self

    def _year_all_loop(self, i: int, year: int, month: int):
        if i < 0:
            return
        save = [year - 50, year - 20, year + 10, year + 40, year + 70]
        self._data.append(
            self._button(lg.get('time.year.select', self._lang, i, i + 9), callback_data=f'{i}/{month}year'))
        if i in save:
            self._save_data()
        pass

    def _save_data(self):
        self._final_data.append(self._data)
        self._data = []
        pass

    def _year(self, year: int, month: int, data: str = 'date-pick'):
        self._data.append(self.create('<', f'{year - 1}/{month}{data}'))
        self._data.append(self._button(lg.get('time.year', self._lang, f"{year}"), callback_data=f'{year}/{month}year'))
        self._data.append(self.create('>', f'{year + 1}/{month}{data}'))
        return self

    def _month(self, year: int, month: int, data: str = 'date-pick'):
        self._data.append(self.create('<', _month_callback(year, month, text=data)))
        self._data.append(self.create(f'time.month.{month}', f'{year}/{month}month'))
        self._data.append(self.create('>', _month_callback(year, month, True, data)))
        return self

    def _style_monday(self, data: list, year: int, month: int):

        self._final_data.extend([
            [
                self.create(f"{value_one if (value_one != 41) and (value_one != 42) else ' '}",
                            _pick_callback(value_one, year, month))
                for value_one, value_two in data_final
            ]
            for data_final in data
        ])
        pass

    def _style_sunday(self, data: list, year: int, month: int, style: int):
        self._final_data.extend(_StyleSunday(data, year, month, self._lang, style))
        pass


def _StyleSunday(data: list[list[tuple[int, int]]], year: int, month: int, lang: str, style: int):
    inner = []
    final = []

    def create(text: str, callback):
        return InlineKeyboardButton(lg.get(text, lang), callback_data=callback)

    def item_loop():
        """
        讀取第二層list資料的for迴圈，
        與 finale 配套
        :return:
        """
        for (value_one, value_two) in data_final:
            item_create(value_one, value_two)
        pass

    def item_create(value_one: int,
                    value_two: int):
        """
        判斷當前位置並給出相應得資料操作，
        與 finale 配套
        :param value_one: 日期
        :param value_two: 星期
        :return:
        """
        nonlocal inner
        inner.append(create(f"{value_one if (value_one != 41) and (value_one != 42) else ' '}",
                            _pick_callback(value_one, year, month)))
        all_empty = all(button.text == ' ' for button in inner)
        if value_one == 41 and value_two == 6 - style:
            inner = []
        elif value_two == 6 - style:
            final.append(inner)
            inner = []
        elif index == len(data) - 1 and value_one == 42 and value_two == 7 - style:
            return
        elif not all_empty and index == len(data) - 1 and value_two == 6:
            inner += [create(" ", _month_callback(year, month, True)) for _ in range(7 - style)]
            final.append(inner)
            inner = []
        pass

    for _ in range(style):
        inner.append(create(" ", _month_callback(year, month)))
    for index, data_final in enumerate(data):
        item_loop()
    return final


def _pick_callback(number: int, year: int, month: int) -> str:
    t = myTime()
    if number == 41 or number == 42:
        return _month_callback(year, month) if number == 41 else _month_callback(year, month, True)
    elif (year > t.year() or
          (year == t.year() and month > t.month()) or
          (year == t.year() and month == t.month() and number >= t.day())):
        return f"{year}/{month}/{number}date_pick"
    return 'empty'


def _month_callback(year: int, month: int, lest_next: bool = False, text: str = 'date-pick') -> str:
    """
    檢查當前選擇是否為12月或1月，用於修改上下個月的callback_data
    :param year:
    :param month:
    :param lest_next: True -> next, False -> lest
    :return:
    """
    if month == 12:
        return f"{year + 1}/1{text}" if lest_next else f"{year}/11{text}"
    elif month == 1:
        return f"{year}/2{text}" if lest_next else f"{year - 1}/12{text}"
    return f"{year}/{month + 1}{text}" if lest_next else f"{year}/{month - 1}{text}"


def _turn(week: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]]:
    """
    將第一天以前的0改為41，
    將最後一天以後的0改為42，
    以提供上下個月切換
    :param week: 原始資料輸入
    :return:
    """
    for row, data1 in enumerate(week):
        week = _data_turn(row, data1, week)
    return week


def _data_turn(row: int,
               data1: list[tuple[int, int]],
               week: list[list[tuple[int, int]]]) -> list[list[tuple[int, int]]]:
    """
    轉換的for迴圈，
    與 _turn 配套
    :param row:
    :param data1:
    :param week:
    :return:
    """
    for i, (one, two) in enumerate(data1):
        if row != 0 or row != len(week) - 1:
            pass
        if one == 0:
            week[row][i] = (41 if row == 0 else 42, two)
    return week


class ShowButton(Button):
    def __init__(self, page: int, user: int, chat: int, isAll: bool, lang: str):
        super().__init__(lang)
        self._isAll = isAll
        self._page = page
        self._replyText = ''
        self._check = f"{user}-{chat}-"
        self._user = user
        self._chat = chat
        self.lang = lang
        self._init()

    def _init(self):
        if self._isAll:
            self.number = sql.showAllNumber()[0][0]
            self.allText = 'all'
        else:
            self.number = sql.showNumber(self._user, self._chat)[0][0]
            self.allText = ''
        self.final = math.ceil(self.number / 10)
        return self

    @DateSelect.tick
    def showMark(self) -> InlineKeyboardMarkup:
        """
        按鈕按下後繼續生成對應之按鈕顯示部分
        :return: InlineKeyboardMarkup
        """
        if self._page == self.final and self._page != 1:
            return self._lestMark()
        elif self.final == 1:
            return self._oneMark()
        elif self._page == 1:
            return self._firstMark()
        return self._middleMark()

    @DateSelect.tick
    def showContext(self, data: list[tuple[int, str, datetime]]) -> str:
        lest: int = 15
        if not data:
            return 'error'
        for index in data:
            text = str(index[1]).replace("\n", " ")[:lest]
            doc = f"{text}{'...' if len(index[1]) > lest else ''}".ljust(lest + 5)
            self._replyText += lg.get('schedule.show.index', self.lang, index[0], doc)
        return self._replyText

    @DateSelect.tick
    def showButton(self) -> InlineKeyboardMarkup | None:
        """
        使用者輸入/show後回根據總頁數回傳按鈕顯示部分
        :return: InlineKeyboardMarkup
        """
        if self.final == 0:
            return None
        elif self.final == 1:
            return self._oneMark()
        return self._firstMark()

    def _oneMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                self.create(' ', f'empty'),
                self.create(' ', f'empty'),
                self.create('↻', f'{self._check}{self.allText}return{self._page}'),
                self.create(' ', f'empty'),
                self.create(' ', f'empty')
            ]
        ])
        return mark

    def _lestMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                self.create('<<', f'{self._check}{self.allText}nextPage{1}'),
                self.create('<', f'{self._check}{self.allText}nextPage{self._page - 1}'),
                self.create('↻', f'{self._check}{self.allText}return{self._page}'),
                self.create(' ', 'empty'),
                self.create(' ', 'empty')
            ]
        ])
        return mark

    def _firstMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                self.create(' ', 'empty'),
                self.create(' ', 'empty'),
                self.create('↻', f'{self._check}{self.allText}return{self._page}'),
                self.create('>', f'{self._check}{self.allText}nextPage{2}'),
                self.create('>>', f'{self._check}{self.allText}nextPage{self.final}')
            ]
        ])
        return mark

    def _middleMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                self.create('<<', f'{self._check}{self.allText}nextPage{1}'),
                self.create('<', f'{self._check}{self.allText}nextPage{self._page - 1}'),
                self.create('↻', f'{self._check}{self.allText}return{self._page}'),
                self.create('>', f'{self._check}{self.allText}nextPage{self._page + 1}'),
                self.create('>>', f'{self._check}{self.allText}nextPage{self.final}')
            ]
        ])
        return mark
