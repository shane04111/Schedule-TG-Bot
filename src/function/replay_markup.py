from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.month_to_day import month_to_day
from src.function.my_time import time_year, time_month, time_day, time_date


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
    get_year = check_YMD().year
    get_month = check_YMD().month
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
    def __init__(self, year, month, is_valid):
        self.year = year
        self.month = month
        self.is_valid = is_valid
