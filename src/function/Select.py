from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.month_to_day import month_to_day
from src.function.replay_markup import buttonBackCancelHandler


def year_select(year, lang):
    """
    輸入年份並輸出設定年份按鈕
    :param lang:
    :param year: 輸入所需之開始年份
    :return:
    """
    year_markup = _select(year, year + 11, 3, 'year', lang)
    return year_markup


def month_select(month, lang):
    """
    輸入月份輸出該月有幾天的按鈕
    :param lang:
    :param month: 月份
    :return:
    """
    month_markup = _select(month, 12, 6, 'month', lang)
    return month_markup


def day_select(year, month, day, lang):
    """
    輸出日期選擇按鈕
    :param lang:
    :param year: 年
    :param month: 月
    :param day: 日
    :return:
    """
    day_markup = _select(day, month_to_day(year, month), 6, 'day', lang)
    return day_markup


def _select(index, max_value: int, inner_list_length: int, callbackText: str, lang: str) -> InlineKeyboardMarkup:
    result = []
    while index <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            _selectDo(index, max_value, inner_list, callbackText, lang)
            index += 1
        result.append(inner_list)
    result.append(buttonBackCancelHandler(f"{callbackText}_back", lang))
    markup = InlineKeyboardMarkup(result)
    return markup


def _selectDo(index, max_value, inner_list, callbackText, lang):
    if index <= max_value:
        inner_list.append(InlineKeyboardButton(
            lg.get(f"button.{callbackText}", lang, str(index)),
            callback_data=f"{index}{callbackText}"
        ))
