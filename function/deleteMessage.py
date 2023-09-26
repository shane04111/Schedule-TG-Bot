from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from function.SQL_Model import GetUserMessage


def CreateDeleteButton(user, chat):
    data = GetUserMessage(user, chat)
    result = []
    n = 20
    if not data:
        inner_list = []
        result.append(inner_list)
    else:
        for index in data:
            inner_list = []
            if len(index[1]) <= n:
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{index[1]}, 提醒時間：{index[2]}", callback_data=f"{index[0]}del"))
            else:
                getString = str(index[1])
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{getString[:n]}...,\n"
                    f"提醒時間：{index[2]}", callback_data=f"{index[0]}del"))
            result.append(inner_list)
    result.append([InlineKeyboardButton("取消", callback_data="del")])
    month_markup = InlineKeyboardMarkup(result)
    return month_markup
