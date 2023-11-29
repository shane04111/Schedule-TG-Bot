from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class Local:
    def __init__(self):
        self._utc = ['UTC+01:00', 'UTC+02:00', 'UTC+03:00', 'UTC+03:30', 'UTC+04:00', 'UTC+04:30', 'UTC+05:00',
                     'UTC+05:30', 'UTC+05:45', 'UTC+06:00', 'UTC+06:30', 'UTC+07:00', 'UTC+08:00', 'UTC+09:00',
                     'UTC+09:30', 'UTC+10:00', 'UTC+10:30', 'UTC+11:00', 'UTC+12:00', 'UTC+12:45', 'UTC+13:00',
                     'UTC+14:00', 'UTC-09:00', 'UTC±00:00', 'UTC−01:00', 'UTC−02:00', 'UTC−03:00', 'UTC−03:30',
                     'UTC−04:00', 'UTC−05:00', 'UTC−06:00', 'UTC−07:00', 'UTC−08:00', 'UTC−09:30', 'UTC−10:00',
                     'UTC−11:00', 'UTC−12:00']
        self.addUtc = ['+01:00', '+02:00', '+03:00', '+03:30', '+04:00', '+04:30', '+05:00', '+05:30', '+05:45',
                       '+06:00', '+06:30', '+07:00', '+08:00', '+09:00', '+09:30', '+10:00', '+10:30', '+11:00',
                       '+12:00', '+12:45', '+13:00', '+14:00', '-09:00', '00:00', '−01:00', '−02:00', '−03:00',
                       '−03:30', '−04:00', '−05:00', '−06:00', '−07:00', '−08:00', '−09:30', '−10:00', '−11:00',
                       '−12:00']

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
                inner_list.append(InlineKeyboardButton(self._utc[index], callback_data=self.addUtc[index]))
                index += 1
            result.append(inner_list)
            i += 1
        markup = InlineKeyboardMarkup(result)
        return markup
