from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from function.my_time import time_year, time_month, time_day
from function.month_to_day import month_to_day

# ======================================================================================

true_false_text_data = [
    [
        InlineKeyboardButton("確認", callback_data='text_true'),
        InlineKeyboardButton("取消", callback_data='text_false')
    ]
]

true_false_text = InlineKeyboardMarkup(true_false_text_data)

# ======================================================================================

TD_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='TD_true'),
        InlineKeyboardButton("否", callback_data='TD_false')
    ]
]

TD_check = InlineKeyboardMarkup(TD_TF_data)

# ======================================================================================

SD_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='SD_true'),
        InlineKeyboardButton("否", callback_data='SD_false')
    ]
]

SD_check = InlineKeyboardMarkup(SD_TF_data)

# ======================================================================================

OY_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='OY_true'),
        InlineKeyboardButton("否", callback_data='OY_false')
    ]
]

OY_check = InlineKeyboardMarkup(OY_TF_data)

# ======================================================================================

ALL_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='ALL_true'),
        InlineKeyboardButton("否", callback_data='ALL_false')
    ]
]

ALL_check = InlineKeyboardMarkup(ALL_TF_data)

# ======================================================================================

year_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='year_true'),
        InlineKeyboardButton("否", callback_data='year_false')
    ]
]

year_check = InlineKeyboardMarkup(year_TF_data)

# ======================================================================================

month_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='month_true'),
        InlineKeyboardButton("否", callback_data='month_false')
    ]
]

month_check = InlineKeyboardMarkup(month_TF_data)

# ======================================================================================

day_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='day_true'),
        InlineKeyboardButton("否", callback_data='day_false')
    ]
]

day_check = InlineKeyboardMarkup(day_TF_data)

# ======================================================================================

HR_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='HR_true'),
        InlineKeyboardButton("否", callback_data='HR_false')
    ]
]

HR_check = InlineKeyboardMarkup(HR_TF_data)

# ======================================================================================

MIN_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='MIN_true'),
        InlineKeyboardButton("否", callback_data='MIN_false')
    ]
]

MIN_check = InlineKeyboardMarkup(MIN_TF_data)

# ======================================================================================

config_TF_data = [
    [
        InlineKeyboardButton("是", callback_data='config_true'),
        InlineKeyboardButton("否", callback_data='config_false'),
        InlineKeyboardButton("取消設定", callback_data='config_cancel')
    ]
]

config_check = InlineKeyboardMarkup(config_TF_data)


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
        [InlineKeyboardButton("自訂義日期", callback_data='all_set')]
    ]
    time_chose = InlineKeyboardMarkup(time_chose_data)
    return time_chose


def check_YMD():
    """
    檢查當前日期是否為當月之最後一天，\n
    如果是則月份加一並回傳True， \n
    如果是今天最後一天則加年份與月份加一並回傳True
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
