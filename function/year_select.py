from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def year_select(year):
    result = []
    i = 0
    max_value = year + 11
    inner_list_length = 6

    while year <= max_value:
        inner_list = []
        for j in range(inner_list_length):
            if year <= max_value:
                inner_list.append(InlineKeyboardButton(
                    f"{year}年", callback_data=f"{year}year"
                ))
            year += 1
        result.append(inner_list)
        i += 1
    result.append([InlineKeyboardButton("回到上一頁", callback_data="year_back")])
    year_markup = InlineKeyboardMarkup(result)
    return year_markup
