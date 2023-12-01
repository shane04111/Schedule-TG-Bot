from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.replay_markup import MarkUp


def convert_to_chinese_time(hour, lang):
    """
    將數字傳換成中文的時間
    :param lang:
    :param hour: 0-23
    :return:
    """
    hour_mapping = {
        0:  lg.get('time.12:00AM', lang),
        1:  lg.get('time.1:00AM', lang),
        2:  lg.get('time.2:00AM', lang),
        3:  lg.get('time.3:00AM', lang),
        4:  lg.get('time.4:00AM', lang),
        5:  lg.get('time.5:00AM', lang),
        6:  lg.get('time.6:00AM', lang),
        7:  lg.get('time.7:00AM', lang),
        8:  lg.get('time.8:00AM', lang),
        9:  lg.get('time.9:00AM', lang),
        10: lg.get('time.10:00AM', lang),
        11: lg.get('time.11:00AM', lang),
        12: lg.get('time.12:00PM', lang),
        13: lg.get('time.1:00PM', lang),
        14: lg.get('time.2:00PM', lang),
        15: lg.get('time.3:00PM', lang),
        16: lg.get('time.4:00PM', lang),
        17: lg.get('time.5:00PM', lang),
        18: lg.get('time.6:00PM', lang),
        19: lg.get('time.7:00PM', lang),
        20: lg.get('time.8:00PM', lang),
        21: lg.get('time.9:00PM', lang),
        22: lg.get('time.10:00PM', lang),
        23: lg.get('time.11:00PM', lang),
    }

    return hour_mapping.get(hour, '無效的小時數')

# ======================================================================================


def hour_select(hour, lang):
    """
    輸出小時選擇按鈕
    :param lang:
    :param hour: 小時
    :return:
    """
    result = []
    max_value = 23
    inner_list_length = 4

    while hour <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if hour <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{convert_to_chinese_time(hour, lang)}", callback_data=f"{hour}hour"))
            hour += 1
        result.append(inner_list)
    result.append(MarkUp(lang).back('HR_back'))
    final_result = InlineKeyboardMarkup(result)
    return final_result
