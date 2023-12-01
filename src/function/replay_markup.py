import math
from calendar import Calendar
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.ScheduleModel import SqlModel
from src.function.month_to_day import month_to_day
from src.function.my_time import time_year, time_month, time_day, time_date, myTime

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

    def choseDate(self) -> InlineKeyboardMarkup:
        """
        判斷時間並返回相對應設定時間按鈕
        :return:
        """
        time_chose_data = [
            [self._button(f"{lg.get('button.set_today', self._lang, time_date().strftime('%Y/%m/%d'))}",
                          callback_data='today')],
            [self._button(f"{lg.get('button.set_day', self._lang, time_date().strftime('%Y/%m'))}",
                          callback_data='set_day')],
            [self._button(f"{lg.get('button.set_year', self._lang, time_date().strftime('%Y'))}",
                          callback_data='only_year')],
            [self._button(f"{lg.get('button.set_all', self._lang)}", callback_data='all_set')],
            self.back('time_back')
        ]
        time_chose = InlineKeyboardMarkup(time_chose_data)
        return time_chose

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
        self._week = [["time.mon", "time.tu", "time.wed", "time.thur", "time.fri", "time.sat", "time.sun"],
                      ["time.sun", "time.mon", "time.tu", "time.wed", "time.thur", "time.fri", "time.sat"]]
        pass

    def _save_data(self):
        self._final_data.append(self._data)
        self._data = []
        return self

    def _year(self, year: int):
        self._data.append(self.create('<', 'lest-year'))
        self._data.append(self._button(lg.get('time.year', self._lang, f"{year}"), callback_data=f'{year}year'))
        self._data.append(self.create('>', 'next-year'))
        return self

    def _month(self, month: int):
        self._data.append(self.create('<', 'lest-month'))
        self._data.append(self.create(f'time.month.{month}', f'{month}month'))
        self._data.append(self.create('>', 'next-month'))
        return self

    def select_day(self, year: int, month: int, style: int = 0 | 1):
        self._year(year)
        self._month(month)
        self._save_data()
        month_week = self.cld.monthdays2calendar(year, month)
        data = _turn(month_week)
        for i in self._week[style]:
            self._data.append(self.create(i, 'empty'))
        self._save_data()
        if style:
            self._style_sunday(data, year, month)
        else:
            self._style_monday(data, year, month)
        self._data.append(self.create('<', f'{year}lest-month'))
        self._data.append(self.create('↻', f'{year}return-month'))
        self._data.append(self.create('>', f'{year}next-month'))
        self._final_data.append(self._data)
        self._final_data.append(MarkUp(self._lang).back('date_chose'))
        return self

    def _style_monday(self, data: list, year: int, month: int):
        self._final_data.extend([
            [
                self.create(f"{value_one if (value_one != 41) and (value_one != 42) else ' '}",
                            _check_callback_data(value_one, year, month))
                for value_one, value_two in data_final
            ]
            for data_final in data
        ])
        pass

    def _style_sunday(self, data: list, year: int, month: int):
        self._final_data.extend(_StyleSunday(self._lang).finale(data, year, month))
        pass

    def final(self):
        return InlineKeyboardMarkup(self._final_data)


class _StyleSunday(Button):
    """
    創建日期按鈕以周日為起始
    """

    def __init__(self, lang):
        super().__init__(lang)
        self._inner = []
        self._final = []
        pass

    def finale(self,
               data: list[list[tuple[int, int]]],
               year: int,
               month: int):
        """
        創建以周日為一周開始之按鈕
        :param data:
        :param year:
        :param month:
        :return:
        """
        self._inner.append(self.create(" ", "lest-month"))
        for index, data_final in enumerate(data):
            self._item_loop(data, index, data_final, year, month)
        return self._final

    def _item_loop(self,
                   week: list[list[tuple[int, int]]],
                   index: int,
                   data_final: list[tuple[int, int]],
                   year: int,
                   month: int):
        """
        讀取第二層list資料的for迴圈，
        與 finale 配套
        :param index: 第一層list當前指標位置
        :param data_final: 當前指標指向的資料
        :param year: user Year
        :param month: user month
        :param day: user day
        :return:
        """
        for (value_one, value_two) in data_final:
            self._item_create(week, value_one, value_two, index, year, month)
        pass

    def _item_create(self,
                     week: list[list[tuple[int, int]]],
                     value_one: int,
                     value_two: int,
                     index, year: int,
                     month: int):
        """
        判斷當前位置並給出相應得資料操作，
        與 finale 配套
        :param value_one: 日期
        :param value_two: 星期
        :param index: 第一層list當前指標位置
        :param year: user Year
        :param month: user month
        :return:
        """
        self._inner.append(self.create(f"{value_one if (value_one != 41) and (value_one != 42) else ' '}",
                                       _check_callback_data(value_one, year, month)))
        if value_one == 41 and value_two == 5:
            self._inner = []
        elif value_two == 5:
            self._final.append(self._inner)
            self._inner = []
        elif index == len(week) - 1 and value_one != 42 and value_two == 6:
            self._inner += [self.create(" ", "next-month") for _ in range(6)]
            self._final.append(self._inner)
            self._inner = []


def _check_callback_data(number: int, year: int, month: int) -> str:
    if number == 41 or number == 42:
        return 'lest-month' if number == 41 else 'next-month'
    elif (year > myTime().year or
          (year == myTime().year and month > myTime().month) or
          (year == myTime().year and month == myTime().month and number >= myTime().day)):
        return f"{year}/{month}/{number}_day_select"
    return 'empty'


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


def check_YMD():
    """
    檢查當前日期是否為當月之最後一天，\n
    如果是則月份加一並回傳True， \n


    如果是今天今年的最後一天則加年份與月份加一並回傳True
    如果不符合上述條件則返回當前年月並回傳False
    :return:
    """
    if time_day() != month_to_day(time_year(), time_month()):
        lest_month = time_month()
        lest_year = time_year()
        tf_check = False
        return DateResult(lest_year, lest_month, tf_check)
    if time_month() == 12 and time_day() == 31:
        lest_month = 1
        lest_year = time_year() + 1
        tf_check = True
        return DateResult(lest_year, lest_month, tf_check)
    lest_month = time_month() + 1
    lest_year = time_year()
    tf_check = True
    return DateResult(lest_year, lest_month, tf_check)


class DateResult:
    def __init__(self, year: int, month: int, is_valid: bool):
        self.year = year
        self.month = month
        self.is_valid = is_valid


class ShowButton:
    def __init__(self, page: int, user: int, chat: int, isAll: bool, lang: str):
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

    def _lestMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('<<', callback_data=f'{self._check}{self.allText}nextPage{1}'),
                InlineKeyboardButton('<', callback_data=f'{self._check}{self.allText}nextPage{self._page - 1}'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}{self.allText}return{self._page}'),
                InlineKeyboardButton(' ', callback_data='empty'),
                InlineKeyboardButton(' ', callback_data='empty')
            ]
        ])
        return mark

    def _firstMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(' ', callback_data='empty'),
                InlineKeyboardButton(' ', callback_data='empty'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}{self.allText}return{self._page}'),
                InlineKeyboardButton('>', callback_data=f'{self._check}{self.allText}nextPage{2}'),
                InlineKeyboardButton('>>', callback_data=f'{self._check}{self.allText}nextPage{self.final}')
            ]
        ])
        return mark

    def _middleMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('<<', callback_data=f'{self._check}{self.allText}nextPage{1}'),
                InlineKeyboardButton('<', callback_data=f'{self._check}{self.allText}nextPage{self._page - 1}'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}{self.allText}return{self._page}'),
                InlineKeyboardButton('>', callback_data=f'{self._check}{self.allText}nextPage{self._page + 1}'),
                InlineKeyboardButton('>>', callback_data=f'{self._check}{self.allText}nextPage{self.final}')
            ]
        ])
        return mark

    def _oneMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(' ', callback_data=f'empty'),
                InlineKeyboardButton(' ', callback_data=f'empty'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}{self.allText}return{self._page}'),
                InlineKeyboardButton(' ', callback_data=f'empty'),
                InlineKeyboardButton(' ', callback_data=f'empty')
            ]
        ])
        return mark

    def showContext(self, data: list[tuple[int, str, datetime]]) -> str:
        lest: int = 15
        if not data:
            return 'error'
        for index in data:
            text = str(index[1]).replace("\n", " ")[:lest]
            doc = f"{text}{'...' if len(index[1]) > lest else ''}".ljust(lest + 5)
            self._replyText += lg.get('schedule.show.index', self.lang, index[0], doc)
        return self._replyText
