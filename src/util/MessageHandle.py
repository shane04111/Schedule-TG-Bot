import re
from datetime import datetime

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.function.ScheduleModel import SqlModel
from src.function.UserDataModel import start
from src.function.UserLocalModel import UserLocal
from src.function.deleteMessage import CreateDeleteButton, CreateRedoButton
from src.function.loggr import logger
from src.function.replay_markup import MarkUp
from src.local.localTime import Local
from src.translator.getLang import Language
from src.util import MessageLen, DEV_array, bot

lc = Local()
lg = Language()
sql = SqlModel()


async def MessageHandle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    檢測使用者輸入訊息，並詢問是否需要提醒
    :param update:
    :param context:
    :return:
    """
    context.bot_data.keys()
    text = None
    update_msg = update.message
    if not update_msg:
        return
    user_id = update_msg.from_user.id
    chat_id = update_msg.chat.id
    local = UserLocal(chat_id)
    language = lg.getDefault(local, update_msg.from_user.language_code)
    if update_msg and update_msg.text:
        text = update_msg.text
    else:
        logger.warning(f"消息為空或無文本內容, user:{user_id}, chat:{chat_id}", exc_info=True)
    id_match = re.search(r'/(\d+)([iI][dD])', text)
    check_commands = r"(![sS]|/[sS])(chedule)?(@EZMinder_bot)?"
    delete_commands = r"(![dD]|/[dD])(elete)?(@EZMinder_bot)?"
    redo_commands = r"(![rR]|/[rR])(edo)?(@EZMinder_bot)?"
    if re.match(check_commands, text):
        await _SetSchedule(update, check_commands, text, user_id, chat_id, language)
    elif re.match(delete_commands, text):
        del_data = sql.GetUserMessage(user_id, chat_id)
        await DoCommands(update, del_data, "delete.start", CreateDeleteButton(user_id, chat_id),
                         user_id, chat_id, language)
    elif re.match(redo_commands, text):
        redo_data = sql.GetUserDoneMessage(user_id, chat_id)
        await DoCommands(update, redo_data, "redo.start", CreateRedoButton(user_id, chat_id),
                         user_id, chat_id, language)
    elif id_match and str(user_id) in DEV_array:
        await searchId(update, id_match, chat_id, user_id, language)
    elif id_match:
        await searchId(update, id_match, chat_id, user_id, language, False)
    elif update_msg.chat.type == "private":
        await startSet(update_msg, text, user_id, chat_id, language)
    else:
        return


async def DoCommands(update: Update,
                     Data: list[tuple[int, str, datetime]],
                     ReplayText: str,
                     ButtonMark: InlineKeyboardMarkup,
                     user_id: int,
                     chat_id: int,
                     lang: str) -> None:
    """
    回復傳入訊息並根據傳入資料建立訊息之按鈕
    :param update:
    :param Data: 數據庫回膗資料
    :param ReplayText: 回復訊息
    :param ButtonMark: 建立按鈕
    :param user_id: 使用者id
    :param chat_id: 頻道id
    :param lang:
    :return:
    """
    if Data:
        text = update.message.text
        user_msg = update.message.message_id
        msg = await update.message.reply_text(lg.get(ReplayText, lang), reply_markup=ButtonMark)
        msg_id = msg.message_id
        start(user_id, chat_id, msg_id, user_msg, text)
    else:
        await update.message.reply_text(lg.get("both.none", lang))


async def _SetSchedule(update: Update,
                       checkCommands: str,
                       text: str,
                       user_id: int,
                       chat_id: int,
                       lang: str) -> None:
    """
    設定提醒事項
    :param update:
    :param checkCommands: 提醒前墜或指令
    :param text: 使用者輸入訊息
    :param user_id: 使用者id
    :param chat_id: 頻道id
    :param lang: 使用者語言
    :return:
    """
    clear_text = re.sub(checkCommands, "", text).strip()
    if clear_text == "":
        user_message = update.message.message_id
        msg = await update.message.reply_text(lg.get("schedule.none.error", lang))
        start(user_id, chat_id, msg.message_id, user_message)
        return
    await startSet(update.message, clear_text, user_id, chat_id, lang)


async def startSet(update,
                   text: str,
                   user: int,
                   chat: int,
                   lang: str) -> None:
    """
    判斷是否過長並給出相對的詢問
    :param update:
    :param text: 使用者輸入之訊息
    :param user: 使用者id
    :param chat: 聊天頻道
    :param lang: 翻譯語言
    :return:
    """
    mark = MarkUp(lang)
    logger.debug(f"len text: {len(text)}")
    user_message = update.message_id
    if len(text) <= MessageLen:
        text1 = f'```\n{text}```'
        msg = await update.reply_markdown_v2(
            lg.get('schedule.reminder.check.short', lang, text1),
            reply_markup=mark.firstCheck())
    else:
        await update.reply_text(text)
        msg = await update.reply_text(lg.get('schedule.reminder.check.long', lang),
                                      reply_markup=mark.firstCheck())
    message_id = msg.message_id
    start(user, chat, message_id, user_message, text)


async def searchId(update: Update,
                   id_match: re.Match,
                   chat_id: int,
                   user_id: int,
                   lang: str,
                   isDEV: bool = True) -> None:
    """
    尋找特定id訊息，並將提醒內容傳給使用者
    :param update:
    :param id_match: 使用者輸入指令
    :param chat_id: 頻道id
    :param user_id: 使用者id
    :param lang:
    :param isDEV: 檢查是否為開發人員
    :return:
    """
    get_need_id = id_match.group(1)
    long_item = None
    data = sql.GetIdData(get_need_id) if isDEV else sql.GetIdUserData(get_need_id, user_id, chat_id)
    if len(data) != 1:
        logger.error(
            f'預期只有一筆資料，但回傳了 {len(data)} 筆資料\ndate: {data}\nFile: "{__file__}",line {"167" if isDEV else "169"}')
        return
    item = data[0]
    if not item:
        await update.message.reply_text(lg.get('id.none', lang, get_need_id))
        return
    if len(item) <= MessageLen:
        formatted_item = lg.get('id.short.reminder', lang, item[2], item[1])
    else:
        formatted_item = lg.get('id.long.reminder', lang, item[2])
        long_item = item[1]
    if long_item is None:
        await update.message.reply_text(lg.get('id.get', lang, get_need_id, formatted_item))
    else:
        await update.message.reply_text(lg.get('id.get', lang, get_need_id, formatted_item))
        await bot.send_message(chat_id, long_item)
