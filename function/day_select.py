from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from function.month_to_day import month_to_day


def day_select(year, month, day):
    """
    輸出日期選擇按鈕
    :param year: 年
    :param month: 月
    :param day: 日
    :return:
    """
    result = []
    i = 0
    max_value = month_to_day(year, month)
    inner_list_length = 6

    while day <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if day <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{day}號", callback_data=f"{day}day"))
            day += 1
        result.append(inner_list)
        i += 1
    result.append([InlineKeyboardButton("回到上一頁", callback_data="day_back")])
    day_markup = InlineKeyboardMarkup(result)
    return day_markup
