from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.function import lg
from src.function.my_time import myTime
from src.function.replay_markup import MarkUp


def check_minute_time(minute, lang):
    """
    分鐘轉換
    :param lang:
    :param minute: 分鐘數
    :return:
    """
    if minute == 0:
        return lg.get("button.minute.zero", lang)
    if 0 < minute < 10:
        return lg.get("button.minute.one", lang, str(minute))
    else:
        return lg.get("button.minute", lang, str(minute))


def minute_select(check_min: bool, lang):
    """
    檢查秒數輸出對應所需的分鐘按鈕 \n
    輸入True，代表當前小時數 \n
    輸入False，則代表非當前小時數 \n
    :param lang:
    :param check_min: True: 判斷秒數，False直接輸出0-59
    :return:
    """
    if check_min:
        if myTime().second() > 30:
            minute = myTime().minute() + 2
        elif myTime().minute() > 58:
            minute = 0
        else:
            minute = myTime().minute() + 1
    else:
        minute = 0
    result = []
    max_value = 59
    inner_list_length = 5

    while minute <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if minute <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{check_minute_time(minute, lang)}", callback_data=f"{minute}min"))
            minute += 1
        result.append(inner_list)
    result.append(MarkUp(lang).back('MIN_back'))
    final_result = InlineKeyboardMarkup(result)

    return final_result


def _minuteDo(minute, max_value, inner_list, lang):
    if minute <= max_value:
        inner_list.append(InlineKeyboardButton(
            f"{check_minute_time(minute, lang)}", callback_data=f"{minute}min"))
    minute += 1
