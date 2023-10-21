from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from src.local import UTC, ADDUTC


class Local:
    def __init__(self):
        self._utc = UTC

    def button(self) -> InlineKeyboardMarkup:
        index = 0
        max_value = len(self._utc) - 1
        inner_list_length = 5
        result = []
        i = 0
        while index <= max_value:
            inner_list = []
            for j in range(inner_list_length):
                if index > max_value:
                    break
                inner_list.append(InlineKeyboardButton(self._utc[index], callback_data=ADDUTC[index]))
                index += 1
            result.append(inner_list)
            i += 1
        markup = InlineKeyboardMarkup(result)
        return markup
