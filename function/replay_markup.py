from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from function.month_to_day import month_to_day
from function.my_time import time_year, time_month, time_day

# ======================================================================================

true_false_text = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("確認", callback_data='text_true'),
        InlineKeyboardButton("取消", callback_data='text_false')
    ]
])

# ======================================================================================

config_check = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("是", callback_data='config_true'),
        InlineKeyboardButton("否", callback_data='config_false')
    ],
    [
        InlineKeyboardButton("返回上一頁", callback_data='config_back'),
        InlineKeyboardButton("取消設定", callback_data='cancel')
    ]
])

# ======================================================================================


def time_chose_data_function():
    """
    判斷時間並返回相對應設定時間按鈕
    :return:
    """
    get_year = check_YMD().year
    get_month = check_YMD().month
    time_chose_data = [
        [InlineKeyboardButton(
            f"設定日期為今天{time_year()}/{time_month()}/{time_day()}", callback_data='today')],
        [InlineKeyboardButton(
            f"自訂義日，設定年份和月份為{get_year}/{get_month}", callback_data='set_day')],
        [InlineKeyboardButton(
            f"自訂義月和日，年設定為{get_year}", callback_data='only_year')],
        [InlineKeyboardButton("自訂義日期", callback_data='all_set')],
        [
            InlineKeyboardButton("返回上一頁", callback_data='time_back'),
            InlineKeyboardButton("取消設定", callback_data='cancel')
        ]
    ]
    time_chose = InlineKeyboardMarkup(time_chose_data)
    return time_chose


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
