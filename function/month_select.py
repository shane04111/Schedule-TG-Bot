from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def month_select(month):
    """
    輸入月份輸出該月有幾天的按鈕
    :param month: 月份
    :return:
    """
    result = []
    i = 0
    max_value = 12
    inner_list_length = 6

    while month <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if month <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{month}月", callback_data=f"{month}month"
                ))
            month += 1
        result.append(inner_list)
        i += 1
    result.append([
        InlineKeyboardButton("回到上一頁", callback_data="month_back"),
        InlineKeyboardButton("取消設定", callback_data='cancel')
    ])
    month_markup = InlineKeyboardMarkup(result)
    return month_markup
