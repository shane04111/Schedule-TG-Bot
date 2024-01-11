from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.function.ScheduleModel import SqlModel

sql = SqlModel()


def CreateDeleteButton(user, chat):
    data = sql.GetUserMessage(user, chat)
    return CreateButton(data, 'del')


def CreateRedoButton(user, chat):
    data = sql.GetUserDoneMessage(user, chat)
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
                new_text = str(index[1]).replace("\n", " ")
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{new_text}, 提醒時間：{index[2]}", callback_data=f"{index[0]}{SetButton}"))
            else:
                get_string = str(index[1]).replace("\n", " ")
                inner_list.append(InlineKeyboardButton(
                    f"提醒事項：{get_string[:n]}...,\n"
                    f"提醒時間：{index[2]}", callback_data=f"{index[0]}{SetButton}"))
            result.append(inner_list)
    result.append([InlineKeyboardButton("取消", callback_data=f"{SetButton}")])
    month_markup = InlineKeyboardMarkup(result)
    return month_markup
