import re
from datetime import datetime

import telegram
from telegram import Update, CallbackQuery, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.function import lg
from src.function.ScheduleModel import sqlModel
from src.function.Select import day_select, month_select, year_select
from src.function.UserDataModel import CheckUser, UserDataInsert, UserData
from src.function.UserLocalModel import UserLocal
from src.function.deleteMessage import CreateDeleteButton
from src.function.hour_select import hour_select, convert_to_chinese_time
from src.function.loggr import logger
from src.function.minute_select import minute_select
from src.function.my_time import time_year, time_month, time_day, time_minute, time_hour
from src.function.replay_markup import time_chose_data_function, true_false_text, check_YMD, config_check, showButton
from src.util import MessageLen, bot

sql = sqlModel()


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
    local = UserLocal(query_chat_id)
    language = lg.getDefault(local, query.from_user.language_code)
    # ==========user_data===========
    key = {
        'user': query_user_id,
        'chat': query_chat_id,
        'message': query_message_id
    }
    userData = CheckUser(query_user_id, query_chat_id, query_message_id)
    insert = UserDataInsert(userData.id)
    # ===========match==============
    year_match = re.search(r'(\d+)year', query.data)
    month_match = re.search(r'(\d+)month', query.data)
    day_match = re.search(r'(\d+)day', query.data)
    hour_match = re.search(r'(\d+)hour', query.data)
    min_match = re.search(r'(\d+)min', query.data)
    delete_match = re.search(r'(\d+)del', query.data)
    redo_match = re.search(r'(\d+)redo', query.data)
    pageMatch = re.search(r'(\d+)-*(\d+)-(all)?nextPage(\d+)', query.data)
    returnMatch = re.search(r'(\d+)-*(\d+)-(all)?return(\d+)', query.data)
    await query.answer()
    if not userData.checkUser:
        return
    if query.data == "text_true":
        await EditMessage(query, lg.get("schedule.check.time", language), time_chose_data_function(language))
    elif query.data == "time_back":
        text = userData.text
        if len(text) <= MessageLen:
            await EditMessage(query, lg.get("schedule.reminder.check.short", language, text), true_false_text(language))
        else:
            await EditMessage(query, lg.get("schedule.reminder.check.long", language), true_false_text(language))
    elif query.data == "today":
        SaveTimeDate(userData, time_year(), time_month(), time_day(), True, False)
        if time_minute() > 57:
            set_select_hour = time_hour() + 1
        else:
            set_select_hour = time_hour()
        await EditMessage(query, lg.get("schedule.hour", language, SendTime(key, 3, language)),
                          hour_select(set_select_hour, language))
    elif query.data == "set_day":
        SaveTimeDate(userData, check_YMD().year, check_YMD().month, -1, False, False)
        if check_YMD().is_valid:
            year_need = check_YMD().year
            month_need = check_YMD().month
            day_need = 1
        else:
            year_need = check_YMD().year
            month_need = check_YMD().month
            day_need = time_day() + 1
        await EditMessage(query, lg.get("schedule.day", language, SendTime(key, 2, language)),
                          day_select(year_need, month_need, day_need, language))
    elif query.data == "only_year":
        SaveTimeDate(userData, check_YMD().year, -1, -1, False, True)
        if check_YMD().is_valid:
            month_need = check_YMD().month
        else:
            month_need = time_month() + 1
        await EditMessage(query, lg.get("schedule.month", language, SendTime(key, 1, language)),
                          month_select(month_need, language))
    elif query.data == "all_set":
        SaveTimeDate(userData, -1, -1, -1, False, True)
        await EditMessage(query, lg.get("schedule.year", language), year_select(time_year() + 1, language))
    elif query.data == "year_back":
        await EditMessage(query, lg.get("schedule.back", language), time_chose_data_function(language))
    elif query.data == "month_back":
        year_need = userData.year
        if year_need == time_year():
            await EditMessage(query, lg.get("schedule.back", language), time_chose_data_function(language))
        else:
            await EditMessage(query, lg.get("schedule.back.month", language, SendTime(key, 1, language)),
                              year_select(time_year() + 1, language))
    elif year_match:
        get_year = int(year_match.group(1))
        insert.Year(get_year).insert()
        await EditMessage(query, lg.get("schedule.match.year", language, f"{get_year}"),
                          month_select(1, language))
    elif month_match:
        get_month = int(month_match.group(1))
        insert.Month(get_month).insert()
        year_need = userData.year
        await EditMessage(query, lg.get("schedule.match.month", language, f"{year_need}/{get_month}"),
                          day_select(year_need, get_month, 1, language))
    elif day_match:
        get_day = int(day_match.group(1))
        insert.Day(get_day).insert()
        await EditMessage(query, lg.get("schedule.hour", language, SendTime(key, 3, language)),
                          hour_select(0, language))
    elif query.data == "day_back":
        if userData.onlyYear:
            month_need = getNeedMonth(userData)
            await EditMessage(query, lg.get("schedule.month", language, SendTime(key, 2, language)),
                              month_select(month_need, language))
        else:
            await EditMessage(query, lg.get("schedule.back", language), time_chose_data_function(language))
    elif hour_match:
        get_hour = int(hour_match.group(1))
        insert.Hour(get_hour).insert()
        await EditMessage(query,
                          lg.get("schedule.minute", language, SendTime(key, 4, language)),
                          hour_check_button(key, language))
    elif query.data == "HR_back":
        if userData.today:
            await EditMessage(query, lg.get("schedule.back", language), time_chose_data_function(language))
        else:
            await hourBack(query, key, userData, language)
    elif min_match:
        get_min = int(min_match.group(1))
        insert.Minute(get_min).insert()
        await EditMessage(query, message_check_text(key, language), config_check(language))
    elif query.data == "MIN_back":
        await EditMessage(query, lg.get("schedule.hour", language, SendTime(key, 4, language)),
                          hour_select(hour_check_need(key), language))
    elif query.data == "config_true":
        FinalSaveData(key)
        await EditMessage(query, lg.get("schedule.done", language))
    elif query.data == "config_false":
        await EditMessage(query, lg.get("schedule.back", language), time_chose_data_function(language))
    elif query.data == "config_back":
        await EditMessage(query, lg.get("schedule.minute", language, SendTime(key, 4, language)),
                          hour_check_button(key, language))
    elif query.data == "cancel":
        insert.done().insert()
        await EditMessage(query, lg.get("schedule.cancel", language))
    elif delete_match:
        get_delete = delete_match.group(1)
        sql.ChangeSendTrue(get_delete)
        DelData = sql.GetUserMessage(query_user_id, query_chat_id)
        if DelData:
            await EditMessage(query, "已刪除所選提醒，還有以下提醒：",
                              CreateDeleteButton(query_user_id, query_chat_id))
        else:
            await EditMessage(query, "無提醒訊息")
    elif query.data == "del":
        await EditMessage(query, "如需重新刪除提醒請再次輸入指令")
    elif redo_match:
        get_redo = redo_match.group(1)
        data = sql.GetIdData(get_redo)
        text = data[0][1]
        insert.Text(text)
        if len(text) >= MessageLen:
            await bot.sendMessage(query_chat_id, text)
            await EditMessage(query, lg.get("schedule.reminder.check.long", language), true_false_text(language))
        else:
            await EditMessage(query, lg.get("schedule.reminder.check.short", language, text), true_false_text(language))
    elif query.data in lg.lang:
        local.language(query.data).update()
        await EditMessage(query, lg.get("local.language.done", query.data))
    elif pageMatch:
        await _showMessage(query, pageMatch, query_user_id, query_chat_id, language)
    elif returnMatch:
        await _showMessage(query, returnMatch, query_user_id, query_chat_id, language)
    elif query.data == 'empty':
        return
    else:
        logger.warning(f"錯誤的按鈕回傳: {query.data}")
        return


async def EditMessage(query: CallbackQuery,
                      editMessage: str,
                      mark: InlineKeyboardMarkup | None = None
                      ) -> None:
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


async def _showMessage(query: CallbackQuery,
                       reInput: re.Match,
                       user: int,
                       chat: int,
                       language: str) -> None:
    page = int(reInput.group(4))
    isAll = reInput.group(3)
    logger.debug(f"{isAll},{type(isAll)}")
    button = showButton(page, user, chat, isAll, language)
    if isAll:
        data = sql.showAllData((page - 1) * 10)
    else:
        data = sql.showData(user, chat, (page - 1) * 10)
    finalText = lg.get('schedule.show', language, button.showContext(data),
                       str(page), str(button.number), str(button.final))
    text = query.message.text
    if text == finalText:
        return
    await EditMessage(query, finalText, button.showMark())


def FinalSaveData(key: dict) -> None:
    """
    將使用者輸入的資料讀取出來並且存入資料庫
    :param key: 使用者資料
    :return:
    """
    data = CheckUser(**key)
    UserDataInsert(data.id).done().insert()
    text = data.text
    userID = data.userID
    chatID = data.chatID
    user_year = data.year
    user_month = data.month
    user_day = data.day
    user_hour = data.hour
    user_minute = data.minute
    sql.SaveData(text, userID, chatID, "%04d" % user_year, "%02d" % user_month, "%02d" % user_day,
                 "%02d" % user_hour, "%02d" % user_minute)


def SendTime(key: dict, nowSet: int, lang: str) -> str:
    """
    回傳當前設定時間
    :param lang:
    :param key:
    :param nowSet:
    :return:
    """
    data = CheckUser(**key)
    year = data.year
    match nowSet:
        case 1:
            return lg.get("schedule.set", lang, f"{year}")
        case 2:
            month = data.month
            return lg.get("schedule.set", lang, f"{year}/{month}")
        case 3:
            month = data.month
            day = data.day
            return lg.get("schedule.set", lang, f"{year}/{month}/{day}")
        case 4:
            month = data.month
            day = data.day
            hour = convert_to_chinese_time(data.hour, lang)
            return lg.get("schedule.set", lang, f"{year}/{month}/{day} {hour}")
        case _:
            return 'error "nowSet" input'


def SaveTimeDate(data: UserData, year: int, month: int, day: int, isToday: bool, isOY: bool) -> None:
    """
    將使用者選取的時間資料傳入data字典中
    :param data: UserData Class
    :param year: 使用者選取年份
    :param month: 使用者選取月份
    :param day: 使用者選取日期
    :param isToday: 使否為今天
    :param isOY:
    :return:
    """
    insert = UserDataInsert(data.id)
    insert.Year(year).Month(month).Day(day).isToday(isToday).isOY(isOY).insert()


def message_check_text(key: dict, lang: str) -> str:
    """
    檢查訊息是否過長，並給出相對應所需之訊息
    :param lang:
    :param key: 使用者按鈕金鑰
    :return:
    """
    data = CheckUser(**key)
    if len(data.text) <= MessageLen:
        edit_message = f"是否選擇{data.year}/{str(data.month).zfill(2)}/{str(data.day).zfill(2)} \
            \n{convert_to_chinese_time(data.hour, lang)}{minute_to_chinese(data.minute, lang)}提醒\n提醒事項：{data.text}"
    else:
        edit_message = f"是否選擇{data.year}/{str(data.month).zfill(2)}/{str(data.day).zfill(2)} \
            \n{convert_to_chinese_time(data.hour, lang)}{minute_to_chinese(data.minute, lang)}提醒\n提醒上述事項"
    return edit_message


def minute_to_chinese(minute: int, lang: str) -> str:
    """
    分鐘轉換
    :param lang:
    :param minute: 分鐘數
    :return:
    """
    if minute == 0:
        return lg.get("time.minute.zero", lang)
    if 0 < minute < 10:
        return lg.get("time.minute.one", lang, str(minute))
    else:
        return lg.get("time.minute", lang, str(minute))


def hour_check_button(key: dict, lang: str) -> InlineKeyboardMarkup:
    """
    檢查時間並輸出按鈕選項
    :param lang:
    :param key:
    :return:
    """
    data = CheckUser(**key)
    if data.today:
        if data.hour == time_hour():
            set_minute_button = minute_select(True, lang)
            return set_minute_button
        else:
            set_minute_button = minute_select(False, lang)
            return set_minute_button
    else:
        set_minute_button = minute_select(False, lang)
        return set_minute_button


def hour_check_need(key: dict) -> int:
    """
    檢查分鐘並給出相應小時
    :param key:
    :return:
    """
    data = CheckUser(**key)
    if data.today:
        if time_minute() > 57:
            set_select_hour = time_hour() + 1
            return set_select_hour
        else:
            set_select_hour = time_hour()
            return set_select_hour
    else:
        set_select_hour = 0
        return set_select_hour


def getNeedMonth(userData: UserData) -> int:
    if time_year() == userData.year:
        if check_YMD().is_valid:
            month_need = check_YMD().month
            return month_need
        else:
            month_need = time_month() + 1
            return month_need
    else:
        month_need = 1
        return month_need


async def hourBack(query: CallbackQuery, key: dict, userData: UserData, lang: str) -> None:
    if time_year() == userData.year and time_month() == userData.month:
        if check_YMD().is_valid:
            month_need = check_YMD().month
            day_need = 1
        else:
            month_need = check_YMD().month
            day_need = time_day() + 1
        await EditMessage(query, lg.get("schedule.day", lang, SendTime(key, 3, lang)),
                          day_select(time_year(), month_need, day_need, lang))
    else:
        await EditMessage(query, lg.get("schedule.day", lang, SendTime(key, 3, lang)),
                          day_select(userData.year, userData.month, 1, lang))
