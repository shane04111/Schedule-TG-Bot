from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from function.month_to_day import month_to_day


def year_select(year):
    """
    輸入年份並輸出設定年份按鈕
    :param year: 輸入所需之開始年份
    :return:
    """
    year_markup = Select(year, year + 11, 6, '年', 'year')
    return year_markup


def month_select(month):
    """
    輸入月份輸出該月有幾天的按鈕
    :param month: 月份
    :return:
    """
    month_markup = Select(month, 12, 6, '月', 'month')
    return month_markup


def day_select(year, month, day):
    """
    輸出日期選擇按鈕
    :param year: 年
    :param month: 月
    :param day: 日
    :return:
    """
    day_markup = Select(day, month_to_day(year, month), 6, '號', 'day')
    return day_markup


def Select(index, max_value: int, inner_list_length: int, showText: str, callbackText: str):
    result = []
    i = 0
    while index <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if index <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{index}{showText}", callback_data=f"{index}{callbackText}"
                ))
            index += 1
        result.append(inner_list)
        i += 1
    result.append([
        InlineKeyboardButton("回到上一頁", callback_data=f"{callbackText}_back"),
        InlineKeyboardButton("取消設定", callback_data='cancel')
    ])
    markup = InlineKeyboardMarkup(result)
    return markup
