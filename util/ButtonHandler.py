import os
import re

import telegram
from dotenv import load_dotenv
from telegram import Update, CallbackQuery, InlineKeyboardMarkup, Bot
from telegram.ext import ContextTypes

from function.SQL_Model import ChangeSendTrue, GetUserMessage, GetIdData, SaveData
from function.Select import day_select, month_select, year_select
from function.deleteMessage import CreateDeleteButton
from function.hour_select import hour_select, convert_to_chinese_time
from function.loggr import logger
from function.minute_select import minute_select
from function.my_time import time_year, time_month, time_day, time_minute, time_hour
from function.replay_markup import time_chose_data_function, true_false_text, check_YMD, config_check
from util.MessageHandle import user_data

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)


async def ScheduleButton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        按鈕檢測及回應
        :param update:
        :param context:
        :return:
        """
    query = update.callback_query
    query_user_id = query.from_user.id
    query_chat_id = query.message.chat.id
    query_message_id = query.message.message_id
    # ==========user_data===========
    query_get_key = f"{query_user_id}|{query_chat_id}|{query_message_id}"
    get_need_data = None
    if query_get_key in user_data:
        get_need_data = user_data[query_get_key]
    else:
        await bot.sendMessage(query_chat_id, "按鈕已過時或無權限")
    # ===========match==============
    day_match = re.search(r'(\d+)day', query.data)
    hour_match = re.search(r'(\d+)hour', query.data)
    min_match = re.search(r'(\d+)min', query.data)
    month_match = re.search(r'(\d+)month', query.data)
    year_match = re.search(r'(\d+)year', query.data)
    delete_match = re.search(r'(\d+)del', query.data)
    redo_match = re.search(r'(\d+)redo', query.data)
    await query.answer()
    if query_get_key in user_data and get_need_data.get('user_id') == query_user_id and get_need_data is not None:
        if query.data == "text_true":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "text_false":
            user_data.pop(query_get_key)
            await EditMessage(query, "結束提醒設定\n如需設定其他提醒請重新使用 /schedule")
        elif query.data == "time_back":
            text = get_need_data["text"]
            if len(text) <= 1900:
                await EditMessage(query, f"請確認提醒事項：{text}", true_false_text)
            else:
                await EditMessage(query, "是否提醒上述事項", true_false_text)
        elif query.data == "today":
            SaveTimeDate(get_need_data, time_year(), time_month(), time_day(), True, False)
            if time_minute() > 57:
                set_select_hour = time_hour() + 1
            else:
                set_select_hour = time_hour()
            await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾點提醒",
                              hour_select(set_select_hour))
        elif query.data == "set_day":
            SaveTimeDate(get_need_data, check_YMD().year, check_YMD().month, "", False, False)
            if check_YMD().is_valid:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = 1
            else:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = time_day() + 1
            await EditMessage(query, f"{SendTime(get_need_data, 2)}\n請選擇要幾號提醒",
                              day_select(year_need, month_need, day_need))
        elif query.data == "only_year":
            SaveTimeDate(get_need_data, check_YMD().year, "", "", False, True)
            if check_YMD().is_valid:
                month_need = check_YMD().month
            else:
                month_need = time_month() + 1
            await EditMessage(query, f"{SendTime(get_need_data, 1)}\n請選擇要幾月提醒",
                              month_select(month_need))
        elif query.data == "all_set":
            SaveTimeDate(get_need_data, check_YMD().year, check_YMD().month, "", False, True)
            await EditMessage(query, "請選擇要幾年提醒", year_select(time_year() + 1))
        elif query.data == "year_back":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "month_back":
            year_need = get_need_data["year"]
            if year_need == time_year():
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
            else:
                await EditMessage(query, f"{SendTime(get_need_data, 1)}\n請選擇要幾年提醒",
                                  year_select(time_year() + 1))
        elif year_match:
            get_year = int(year_match.group(1))
            get_need_data["year"] = get_year
            await EditMessage(query, f"當前選擇時間 {get_year}\n請選擇要幾月提醒", month_select(1))
        elif month_match:
            get_month = int(month_match.group(1))
            get_need_data["month"] = get_month
            year_need = get_need_data["year"]
            await EditMessage(query, f"當前選擇時間 {year_need}/{get_month}\n請選擇要幾號提醒",
                              day_select(year_need, get_month, 1))
        elif day_match:
            get_day = int(day_match.group(1))
            get_need_data["day"] = get_day
            await EditMessage(query, f"{SendTime(get_need_data, 3)}", hour_select(0))
        elif query.data == "day_back":
            if get_need_data["isOY"]:
                if time_year() == get_need_data["year"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                    else:
                        month_need = time_month() + 1
                else:
                    month_need = 1
                await EditMessage(query, f"{SendTime(get_need_data, 2)}\n請選擇要幾月提醒",
                                  month_select(month_need))
            else:
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif hour_match:
            get_hour = int(hour_match.group(1))
            get_need_data["hour"] = get_hour
            await EditMessage(query,
                              f"{SendTime(get_need_data, 4)}\n請選擇要幾分提醒",
                              hour_check_button(get_need_data))
        elif query.data == "HR_back":
            if get_need_data["is_today"]:
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
            else:
                if time_year() == get_need_data["year"] and time_month() == get_need_data["month"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                        day_need = 1
                    else:
                        month_need = check_YMD().month
                        day_need = time_day() + 1
                    await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾號提醒",
                                      day_select(time_year(), month_need, day_need))
                else:
                    await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾號提醒",
                                      day_select(get_need_data["year"], get_need_data["month"],
                                                 1))
        elif min_match:
            get_min = int(min_match.group(1))
            get_need_data["minute"] = get_min
            await EditMessage(query, message_check_text(get_need_data), config_check)
        elif query.data == "MIN_back":
            await EditMessage(query, f"{SendTime(get_need_data, 4)}\n請選擇要幾點提醒",
                              hour_select(hour_check_need(get_need_data)))
        elif query.data == "config_true":
            FinalSaveData(get_need_data)
            user_data.pop(query_get_key)
            await EditMessage(query, "已成功安排提醒\n如需設定其他提醒請再次輸入 /schedule")
        elif query.data == "config_false":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "config_back":
            await EditMessage(query, f"{SendTime(get_need_data, 4)}\n請選擇要幾分提醒",
                              hour_check_button(get_need_data))
        elif query.data == "cancel":
            user_data.pop(query_get_key)
            await EditMessage(query, "已取消安排提醒\n如需設定其他提醒請再次輸入 /schedule")
        elif delete_match:
            get_delete = str(delete_match.group(1))
            ChangeSendTrue(get_delete)
            DelData = GetUserMessage(query_user_id, query_chat_id)
            if DelData:
                await EditMessage(query, "已刪除所選提醒，還有以下提醒：",
                                  CreateDeleteButton(query_user_id, query_chat_id))
            else:
                await EditMessage(query, "無提醒訊息")
        elif query.data == "del":
            await EditMessage(query, "如需重新刪除提醒請再次輸入指令")
        elif redo_match:
            get_redo = str(redo_match.group(1))
            data = GetIdData(get_redo)
            text = data[0][1]
            get_need_data["text"] = text
            if len(text) >= 1900:
                await bot.sendMessage(query_chat_id, text)
                await EditMessage(query, "是否提醒上述事項", true_false_text)
            else:
                await EditMessage(query, f"請確認提醒事項：{text}", true_false_text)
        else:
            logger.warning(f"錯誤的按鈕回傳: {query.data}")
            return
    else:
        return


async def EditMessage(query: CallbackQuery, editMessage: str, mark: InlineKeyboardMarkup = None):
    """
    抓取編輯訊息錯誤, 以避免使用者點及兩次按鈕
    :param query:
    :param editMessage: 編輯訊息內容
    :param mark: 編輯訊息按鈕
    :return:
    """
    try:
        await query.edit_message_text(editMessage, reply_markup=mark)
    except telegram.error.BadRequest:
        logger.warning('機器人嘗試編輯訊息錯誤')
        return


def FinalSaveData(data):
    """
    將使用者輸入的資料讀取出來並且存入資料庫
    :param data: 使用者資料
    :return:
    """
    text = data["text"]
    userID = data["user_id"]
    chatid = data["chat_id"]
    user_year = data["year"]
    user_month = data["month"]
    user_day = data["day"]
    user_hour = data["hour"]
    user_minute = data["minute"]
    SaveData(text, userID, chatid, "%04d" % user_year, "%02d" % user_month, "%02d" % user_day,
             "%02d" % user_hour, "%02d" % user_minute)


def SendTime(data, nowSet: int):
    """
    回傳當前設定時間
    :param data:
    :param nowSet:
    :return:
    """
    year = data["year"]
    match nowSet:
        case 1:
            return f"當前選擇時間 {year}"
        case 2:
            month = data["month"]
            return f"當前選擇時間 {year}/{month}"
        case 3:
            month = data["month"]
            day = data["day"]
            return f"當前選擇時間 {year}/{month}/{day}"
        case 4:
            month = data["month"]
            day = data["day"]
            hour = convert_to_chinese_time(data["hour"])
            return f"當前選擇時間 {year}/{month}/{day} {hour}"
        case _:
            return 'error "nowSet" input'


def SaveTimeDate(data, year: str, month: str, day: str, isToday: bool, isOY: bool):
    """
    將使用者選取的時間資料傳入data字典中
    :param data: 字典
    :param year: 使用者選取年份
    :param month: 使用者選取月份
    :param day: 使用者選取日期
    :param isToday: 使否為今天
    :param isOY:
    :return:
    """
    data.update({
        "year": year,
        "month": month,
        "day": day,
        "is_today": isToday,
        "isOY": isOY
    })


def message_check_text(data):
    """
    檢查訊息是否過長，並給出相對應所需之訊息
    :param data: 使用者輸入資料
    :return:
    """
    if len(data['text']) <= 1900:
        edit_message = f"是否選擇{data['year']}/{str(data['month']).zfill(2)}/{str(data['day']).zfill(2)} \
            \n{convert_to_chinese_time(data['hour'])}{minute_to_chinese(data['minute'])}提醒\n提醒事項：{data['text']}"
    else:
        edit_message = f"是否選擇{data['year']}/{str(data['month']).zfill(2)}/{str(data['day']).zfill(2)} \
            \n{convert_to_chinese_time(data['hour'])}{minute_to_chinese(data['minute'])}提醒\n提醒上述事項"
    return edit_message


def minute_to_chinese(minute):
    """
    分鐘轉換
    :param minute: 分鐘數
    :return:
    """
    if minute == 0:
        return "整"
    if 0 < minute < 10:
        return f"0{minute}分"
    else:
        return f"{minute}分"


def hour_check_button(data):
    """
    檢查時間並輸出按鈕選項
    :param data:
    :return:
    """
    if data["is_today"]:
        if data["hour"] == time_hour():
            set_minute_button = minute_select(True)
            return set_minute_button
        else:
            set_minute_button = minute_select(False)
            return set_minute_button
    else:
        set_minute_button = minute_select(False)
        return set_minute_button


def hour_check_need(data):
    """
    檢查分鐘並給出相應小時
    :param data:
    :return:
    """
    if data["is_today"]:
        if time_minute() > 57:
            set_select_hour = time_hour() + 1
            return set_select_hour
        else:
            set_select_hour = time_hour()
            return set_select_hour
    else:
        set_select_hour = 0
        return set_select_hour
