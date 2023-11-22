import math
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.ScheduleModel import sqlModel
from src.function.month_to_day import month_to_day
from src.function.my_time import time_year, time_month, time_day, time_date

sql = sqlModel()


class MarkUp:
    def __init__(self, lang):
        self._lang = lang

    def firstCheck(self) -> InlineKeyboardMarkup:
        TF = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(lg.get("button.text.true", self._lang), callback_data='text_true'),
                InlineKeyboardButton(lg.get("button.text.false", self._lang), callback_data='cancel')
            ]
        ])
        return TF

    def finalCheck(self) -> InlineKeyboardMarkup:
        check = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(lg.get("button.config.true", self._lang), callback_data='config_true'),
                InlineKeyboardButton(lg.get("button.config.false", self._lang), callback_data='config_false')
            ],
            buttonBackCancelHandler('config_back', self._lang)
        ])
        return check

    def choseDate(self) -> InlineKeyboardMarkup:
        """
        判斷時間並返回相對應設定時間按鈕
        :return:
        """
        time_chose_data = [
            [InlineKeyboardButton(
                f"{lg.get('button.set_today', self._lang, time_date().strftime('%Y/%m/%d'))}", callback_data='today')],
            [InlineKeyboardButton(
                f"{lg.get('button.set_day', self._lang, time_date().strftime('%Y/%m'))}", callback_data='set_day')],
            [InlineKeyboardButton(
                f"{lg.get('button.set_year', self._lang, time_date().strftime('%Y'))}", callback_data='only_year')],
            [InlineKeyboardButton(f"{lg.get('button.set_all', self._lang)}", callback_data='all_set')],
            buttonBackCancelHandler('time_back', self._lang)
        ]
        time_chose = InlineKeyboardMarkup(time_chose_data)
        return time_chose


def true_false_text(lang) -> InlineKeyboardMarkup:
    TF = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(lg.get("button.text.true", lang), callback_data='text_true'),
            InlineKeyboardButton(lg.get("button.text.false", lang), callback_data='cancel')
        ]
    ])
    return TF


def config_check(lang) -> InlineKeyboardMarkup:
    check = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(lg.get("button.config.true", lang), callback_data='config_true'),
            InlineKeyboardButton(lg.get("button.config.false", lang), callback_data='config_false')
        ],
        buttonBackCancelHandler('config_back', lang)
    ])
    return check


def time_chose_data_function(lang) -> InlineKeyboardMarkup:
    """
    判斷時間並返回相對應設定時間按鈕
    :param lang:
    :return:
    """
    time_chose_data = [
        [InlineKeyboardButton(
            f"{lg.get('button.set_today', lang, time_date().strftime('%Y/%m/%d'))}", callback_data='today')],
        [InlineKeyboardButton(
            f"{lg.get('button.set_day', lang, time_date().strftime('%Y/%m'))}", callback_data='set_day')],
        [InlineKeyboardButton(
            f"{lg.get('button.set_year', lang, time_date().strftime('%Y'))}", callback_data='only_year')],
        [InlineKeyboardButton(f"{lg.get('button.set_all', lang)}", callback_data='all_set')],
        buttonBackCancelHandler('time_back', lang)
    ]
    time_chose = InlineKeyboardMarkup(time_chose_data)
    return time_chose


def buttonBackCancelHandler(data: str, lang: str) -> list[InlineKeyboardButton]:
    BC = [
        InlineKeyboardButton(lg.get('button.back', lang), callback_data=data),
        InlineKeyboardButton(lg.get('button.cancel', lang), callback_data='cancel')
    ]
    return BC


def check_YMD():
    """
    檢查當前日期是否為當月之最後一天，\n
    如果是則月份加一並回傳True， \n
    如果是今天今年的最後一天則加年份與月份加一並回傳True
    如果不符合上述條件則返回當前年月並回傳False
    :return:
    """
    if time_day() == month_to_day(time_year(), time_month()):
        if time_month() == 12 and time_day() == 31:
            lest_month = 1
            lest_year = time_year() + 1
            TF_check = True
            return DateResult(lest_year, lest_month, TF_check)
        else:
            lest_month = time_month() + 1
            lest_year = time_year()
            TF_check = True
            return DateResult(lest_year, lest_month, TF_check)
    else:
        lest_month = time_month()
        lest_year = time_year()
        TF_check = False
        return DateResult(lest_year, lest_month, TF_check)


class DateResult:
    def __init__(self, year: int, month: int, is_valid: bool):
        self.year = year
        self.month = month
        self.is_valid = is_valid


class showButton:
    def __init__(self, page: int, user: int, chat: int):
        self._page = page
        self.number = sql.showNumber(user, chat)[0][0]
        self.final = math.ceil(self.number / 10)
        self._replyText = ''
        self._check = f"{user}-{chat}-"

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
                InlineKeyboardButton('<<', callback_data=f'{self._check}nextPage{1}'),
                InlineKeyboardButton('<', callback_data=f'{self._check}nextPage{self._page - 1}'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}return{self._page}'),
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
                InlineKeyboardButton('↻', callback_data=f'{self._check}return{self._page}'),
                InlineKeyboardButton('>', callback_data=f'{self._check}nextPage{2}'),
                InlineKeyboardButton('>>', callback_data=f'{self._check}nextPage{self.final}')
            ]
        ])
        return mark

    def _middleMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('<<', callback_data=f'{self._check}nextPage{1}'),
                InlineKeyboardButton('<', callback_data=f'{self._check}nextPage{self._page - 1}'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}return{self._page}'),
                InlineKeyboardButton('>', callback_data=f'{self._check}nextPage{self._page + 1}'),
                InlineKeyboardButton('>>', callback_data=f'{self._check}nextPage{self.final}')
            ]
        ])
        return mark

    def _oneMark(self) -> InlineKeyboardMarkup:
        mark = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(' ', callback_data=f'empty'),
                InlineKeyboardButton(' ', callback_data=f'empty'),
                InlineKeyboardButton('↻', callback_data=f'{self._check}return{self._page}'),
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
            doc = f"{text}{'...' if len(index[1]) > lest else ''}"
            self._replyText += f"/{index[0]}id\n提醒內容: {doc.ljust(lest + 5)}\n\n"
        return self._replyText
