from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from function.SQL_Model import GetUserMessage, GetUserDoneMessage


def CreateDeleteButton(user, chat):
    data = GetUserMessage(user, chat)
    return CreateButton(data, 'del')


def CreateRedoButton(user, chat):
    data = GetUserDoneMessage(user, chat)
    return CreateButton(data, 'redo')


def CreateButton(data, SetButton):
    result = []
    n = 20
    if not data:
        inner_list = []
        result.append(inner_list)
    else:
        for index in data:
            inner_list = []
            if len(index[1]) <= n:
                newText = str(index[1]).replace("\n", " ")
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{newText}, 提醒時間：{index[2]}", callback_data=f"{index[0]}{SetButton}"))
            else:
                getString = str(index[1]).replace("\n", " ")
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{getString[:n]}...,\n"
                    f"提醒時間：{index[2]}", callback_data=f"{index[0]}{SetButton}"))
            result.append(inner_list)
    result.append([InlineKeyboardButton("取消", callback_data=f"{SetButton}")])
    month_markup = InlineKeyboardMarkup(result)
    return month_markup
