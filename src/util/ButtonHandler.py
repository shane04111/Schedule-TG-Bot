import re

import telegram
from telegram import Update, CallbackQuery, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.function import lg
from src.function.ScheduleModel import SqlModel
from src.function.UserDataModel import CheckUser, UserDataInsert
from src.function.UserLocalModel import UserLocal
from src.function.deleteMessage import CreateDeleteButton
from src.function.hour_select import hour_select, convert_to_chinese_time
from src.function.loggr import logger
from src.function.minute_select import minute_select
from src.function.my_time import myTime
from src.function.replay_markup import ShowButton, MarkUp, DateSelect
from src.util import MessageLen, bot

sql = SqlModel()
time = myTime()


async def ScheduleButton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        按鈕檢測及回應
        :param update:
        :param context:
        :return:
    """
    context.bot_data.keys()
    query = update.callback_query
    query_user_id = query.from_user.id
    query_chat_id = query.message.chat.id
    query_message_id = query.message.message_id
    local = UserLocal(query_chat_id, query_user_id)
    language = lg.getDefault(local, query.from_user.language_code)
    mark = MarkUp(language)
    # ==========user_data===========
    key = {
        'user': query_user_id,
        'chat': query_chat_id,
        'message': query_message_id
    }
    user_data = CheckUser(query_user_id, query_chat_id, query_message_id)
    insert = UserDataInsert(user_data.id)
    date_pick = DateSelect(language)
    # ===========match==============
    date_match = re.search(r'(\d+)/(\d+)/(\d+)date_pick', query.data)
    hour_match = re.search(r'(\d+)hour', query.data)
    min_match = re.search(r'(\d+)min', query.data)
    await query.answer()
    if not user_data.checkUser:
        return
    # schedule button
    if query.data == "text_true":
        await _date_pick(query, language, date_pick.date_pick(time.year, time.month, local.Style).final())
        return
    elif query.data == 'save':
        text = user_data.text
        t = myTime()
        sql.SaveData(text, query_user_id, query_chat_id, "%04d" % t.year, "%02d" % t.month, "%02d" % t.day,
                     "%02d" % t.hour, "%02d" % t.minute, True)
        await _edit_message(query, lg.get("schedule.done", language))
        return
    # date pick controller
    date_pick_match = re.search(r'(\d+)/(\d+)date-pick', query.data)
    pick_style = re.search(r'(\d+)/(\d+)-(\d)week', query.data)
    pick_month = re.search(r'(\d+)/(\d+)month', query.data)
    pick_year = re.search(r'(\d+)/(\d+)year', query.data)
    pick_year_all = re.search(r'(\d+)/(\d+)all-year', query.data)
    if date_pick_match:
        year = int(date_pick_match.group(1))
        month = int(date_pick_match.group(2))
        await _date_pick(query, language, date_pick.date_pick(year, month, local.Style).final())
        return
    elif pick_style:
        year = int(pick_style.group(1))
        month = int(pick_style.group(2))
        style = int(pick_style.group(3))
        local.datePickStyle(style).update()
        await _date_pick(query, language,
                         date_pick.date_pick(year, month, UserLocal(query_chat_id, query_user_id).Style).final())
        return
    elif pick_month:
        year = int(pick_month.group(1))
        month = int(pick_month.group(2))
        await _date_pick(query, language, date_pick.select_month(year, month).final())
        return
    elif pick_year:
        year = int(pick_year.group(1))
        month = int(pick_year.group(2))
        await _date_pick(query, language, date_pick.select_year(year, month).final())
        return
    elif pick_year_all:
        year = int(pick_year_all.group(1))
        month = int(pick_year_all.group(2))
        await _date_pick(query, language, date_pick.year_all(year, month).final())
        return
    # time pick controller
    if date_match:
        year = int(date_match.group(1))
        month = int(date_match.group(2))
        day = int(date_match.group(3))
        insert.Year(year).Month(month).Day(day).insert()
        await _edit_message(query, lg.get("schedule.hour", language, _send_time(key, 3, language)),
                            hour_select(0, language))
        return
    elif query.data == "date_chose":
        text = user_data.text
        if len(text) <= MessageLen:
            await _edit_message(query, lg.get("schedule.reminder.check.short", language, text), mark.firstCheck())
            return
        await _edit_message(query, lg.get("schedule.reminder.check.long", language), mark.firstCheck())
        return
    elif hour_match:
        get_hour = int(hour_match.group(1))
        insert.Hour(get_hour).insert()
        await _edit_message(query,
                            lg.get("schedule.minute", language, _send_time(key, 4, language)),
                            _hour_check_button(key, language))
        return
    elif query.data == "HR_back":
        year = user_data.year
        month = user_data.month
        await _date_pick(query, language, date_pick.date_pick(year, month, local.Style).final())
        return
    elif min_match:
        get_min = int(min_match.group(1))
        insert.Minute(get_min).insert()
        await _edit_message(query, _message_check_text(key, language), mark.finalCheck())
        return
    elif query.data == "MIN_back":
        await _edit_message(query, lg.get("schedule.hour", language, _send_time(key, 4, language)),
                            hour_select(_hour_check_need(key), language))
        return
    # final controller
    if query.data == "config_true":
        _final_save_data(key)
        await _edit_message(query, lg.get("schedule.done", language))
        return
    elif query.data == "config_false":
        year = user_data.year
        month = user_data.month
        style = local.Style
        await _edit_message(query, lg.get("schedule.back", language), date_pick.date_pick(year, month, style))
        return
    elif query.data == "config_back":
        await _edit_message(query, lg.get("schedule.minute", language, _send_time(key, 4, language)),
                            _hour_check_button(key, language))
        return
    elif query.data == "cancel":
        insert.done().insert()
        await _edit_message(query, lg.get("schedule.cancel", language))
        return
    # delete and redo button
    delete_match = re.search(r'(\d+)del', query.data)
    redo_match = re.search(r'(\d+)redo', query.data)
    if delete_match:
        get_delete = delete_match.group(1)
        sql.ChangeSendTrue(get_delete)
        del_data = sql.GetUserMessage(query_user_id, query_chat_id)
        if del_data:
            await _edit_message(query, "已刪除所選提醒，還有以下提醒：",
                                CreateDeleteButton(query_user_id, query_chat_id))
            return
        await _edit_message(query, "無提醒訊息")
        return
    elif query.data == "del":
        await _edit_message(query, "如需重新刪除提醒請再次輸入指令")
        return
    elif redo_match:
        get_redo = redo_match.group(1)
        data = sql.GetIdData(get_redo)
        if len(data) != 1:
            logger.error(f'預期只有一筆資料，但回傳了 {len(data)} 筆資料\ndate: {data}\nFile: "{__file__}",line 121')
            return
        text = data[0][1]
        insert.Text(text)
        if len(text) >= MessageLen:
            await bot.sendMessage(query_chat_id, text)
            await _edit_message(query, lg.get("schedule.reminder.check.long", language), mark.firstCheck())
            return
        await _edit_message(query, lg.get("schedule.reminder.check.short", language, text), mark.firstCheck())
        return
    # local button
    # TODO: user localtime
    if query.data in lg.lang:
        local.language(query.data).update()
        await _edit_message(query, lg.get("local.language.done", query.data))
        return
    # show button
    page_match = re.search(r'(\d+)-*(\d+)-(all)?nextPage(\d+)', query.data)
    return_match = re.search(r'(\d+)-*(\d+)-(all)?return(\d+)', query.data)
    if page_match:
        await _show_message(query, page_match, query_user_id, query_chat_id, language)
        return
    elif return_match:
        await _show_message(query, return_match, query_user_id, query_chat_id, language)
        return
    elif query.data == 'empty':
        return
    logger.debug(f"錯誤的按鈕回傳: {query.data}")
    return


async def _edit_message(query: CallbackQuery,
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
        logger.debug('機器人嘗試編輯訊息錯誤')
        return


async def _date_pick(query: CallbackQuery, lang: str, callback: InlineKeyboardMarkup):
    await _edit_message(query, lg.get('time.select', lang), callback)
    return


async def _show_message(query: CallbackQuery,
                        reInput: re.Match,
                        user: int,
                        chat: int,
                        language: str) -> None:
    page = int(reInput.group(4))
    is_all = reInput.group(3)
    logger.debug(f"{is_all},{type(is_all)}")
    button = ShowButton(page, user, chat, is_all, language)
    if is_all:
        data = sql.showAllData((page - 1) * 10)
    else:
        data = sql.showData(user, chat, (page - 1) * 10)
    final_text = lg.get('schedule.show', language, button.showContext(data),
                        str(page), str(button.number), str(button.final))
    text = query.message.text
    if text == final_text:
        return
    await _edit_message(query, final_text, button.showMark())


def _final_save_data(key: dict) -> None:
    """
    將使用者輸入的資料讀取出來並且存入資料庫
    :param key: 使用者資料
    :return:
    """
    data = CheckUser(**key)
    UserDataInsert(data.id).done().insert()
    text = data.text
    user_id = data.userID
    chat_id = data.chatID
    user_year = data.year
    user_month = data.month
    user_day = data.day
    user_hour = data.hour
    user_minute = data.minute
    sql.SaveData(text, user_id, chat_id, "%04d" % user_year, "%02d" % user_month, "%02d" % user_day,
                 "%02d" % user_hour, "%02d" % user_minute)


def _send_time(key: dict, nowSet: int, lang: str) -> str:
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


def _message_check_text(key: dict, lang: str) -> str:
    """
    檢查訊息是否過長，並給出相對應所需之訊息
    :param lang:
    :param key: 使用者按鈕金鑰
    :return:
    """
    data = CheckUser(**key)
    if len(data.text) <= MessageLen:
        edit_message = f"是否選擇{data.year}/{str(data.month).zfill(2)}/{str(data.day).zfill(2)} \
            \n{convert_to_chinese_time(data.hour, lang)}{_minute_to_chinese(data.minute, lang)}提醒\n提醒事項：{data.text}"
    else:
        edit_message = f"是否選擇{data.year}/{str(data.month).zfill(2)}/{str(data.day).zfill(2)} \
            \n{convert_to_chinese_time(data.hour, lang)}{_minute_to_chinese(data.minute, lang)}提醒\n提醒上述事項"
    return edit_message


def _minute_to_chinese(minute: int, lang: str) -> str:
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


def _hour_check_button(key: dict, lang: str) -> InlineKeyboardMarkup:
    """
    檢查時間並輸出按鈕選項
    :param lang:
    :param key:
    :return:
    """
    data = CheckUser(**key)
    if data.today:
        if data.hour == time.hour:
            set_minute_button = minute_select(True, lang)
            return set_minute_button
        set_minute_button = minute_select(False, lang)
        return set_minute_button
    else:
        set_minute_button = minute_select(False, lang)
        return set_minute_button


def _hour_check_need(key: dict) -> int:
    """
    檢查分鐘並給出相應小時
    :param key:
    :return:
    """
    data = CheckUser(**key)
    if data.today:
        if time.minute > 57:
            set_select_hour = time.hour + 1
            return set_select_hour
        set_select_hour = time.hour
        return set_select_hour
    else:
        set_select_hour = 0
        return set_select_hour
