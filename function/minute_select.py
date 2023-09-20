from telegram import InlineKeyboardButton
from function.my_time import time_minute, time_second


def check_minute_time(minute):
    if minute == 0:
        return "整點"
    if minute > 0 and minute < 10:
        return f"0{minute}分"
    else:
        return f"{minute}分"


def minute_select(check_min: bool):
    if check_min:
        if time_second() > 30:
            minute = time_minute() + 2
        elif time_minute() > 58:
            minute = 0
        else:
            minute = time_minute() + 1
    else:
        minute = 0
    result = []
    i = 0
    max_value = 59
    inner_list_length = 8

    while minute <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if minute <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{check_minute_time(minute)}", callback_data=f"{minute}min"))
            minute += 1
        result.append(inner_list)
        i += 1
    result.append([InlineKeyboardButton("回到上一頁", callback_data="MIN_back")])

    return result
