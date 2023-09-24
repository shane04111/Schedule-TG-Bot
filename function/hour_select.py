from telegram import InlineKeyboardButton


def convert_to_chinese_time(hour):
    """
    將數字傳換成中文的時間
    :param hour: 0-23
    :return:
    """
    hour_mapping = {
        0: '半夜十二點',
        1: '凌晨一點',
        2: '凌晨二點',
        3: '凌晨三點',
        4: '凌晨四點',
        5: '凌晨五點',
        6: '早上六點',
        7: '早上七點',
        8: '早上八點',
        9: '早上九點',
        10: '上午十點',
        11: '上午十一點',
        12: '中午十二點',
        13: '下午一點',
        14: '下午二點',
        15: '下午三點',
        16: '下午四點',
        17: '下午五點',
        18: '晚上六點',
        19: '晚上七點',
        20: '晚上八點',
        21: '晚上九點',
        22: '晚上十點',
        23: '晚上十一點',
    }

    return hour_mapping.get(hour, '無效的小時數')

# ======================================================================================


def hour_select(hour):
    """
    輸出小時選擇按鈕
    :param hour: 小時
    :return:
    """
    result = []
    i = 0
    max_value = 23
    inner_list_length = 4

    while hour <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if hour <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{convert_to_chinese_time(hour)}", callback_data=f"{hour}hour"))
            hour += 1
        result.append(inner_list)
        i += 1
    result.append([InlineKeyboardButton("回到上一頁", callback_data="HR_back")])

    return result
