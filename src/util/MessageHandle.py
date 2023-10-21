import re

from telegram import Update
from telegram.ext import ContextTypes

from src.function.ScheduleModel import GetUserMessage, GetUserDoneMessage, GetIdData, GetIdUserData
from src.function.UserDataModel import ScheduleStart, DoDataInsert
from src.function.UserLocalModel import UserLocal
from src.function.deleteMessage import CreateDeleteButton, CreateRedoButton
from src.function.loggr import logger
from src.function.replay_markup import true_false_text
from src.util import MessageLen, DEV_ID, DEV_array, bot
from src.local.localTime import Local
from src.translator.getLang import Language

lc = Local()
lg = Language()


async def MessageHandle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    檢測使用者輸入訊息，並詢問是否需要提醒
    :param update:
    :param context:
    :return:
    """
    text = None
    updateMsg = update.message
    user_id = updateMsg.from_user.id
    chat_id = updateMsg.chat.id
    local = UserLocal(chat_id)
    language = lg.getDefault(local, updateMsg.from_user.language_code)
    if updateMsg and updateMsg.text:
        text = updateMsg.text
    else:
        logger.warning(f"消息為空或無文本內容, user:{user_id}, chat:{chat_id}", exc_info=True)
    DelData = GetUserMessage(user_id, chat_id)
    RedoData = GetUserDoneMessage(user_id, chat_id)
    id_match = re.search(r'/(\d+)([iI][dD])', text)
    checkCommands = r"(![sS]|/[sS])(chedule)?(@EZMinder_bot)?"
    deleteCommands = r"(![dD]|/[dD])(elete)?(@EZMinder_bot)?"
    redoCommands = r"(![rR]|/[rR])(edo)?(@EZMinder_bot)?"
    # TODO: user Local language and time
    if text == "!id" and str(user_id) == DEV_ID:
        await updateMsg.reply_text(f"{updateMsg.message_id}")
    elif text == "/default":
        msg = await updateMsg.reply_text(lg.get("local.group", language))
        DoDataInsert().init(user_id, chat_id, msg.message_id)
    elif re.match(checkCommands, text):
        await SetSchedule(update, checkCommands, text, user_id, chat_id, language)
    elif re.match(deleteCommands, text):
        await DoCommands(update, DelData, "delete.start", CreateDeleteButton(user_id, chat_id),
                         user_id, chat_id, language)
    elif re.match(redoCommands, text):
        await DoCommands(update, RedoData, "redo.start", CreateRedoButton(user_id, chat_id),
                         user_id, chat_id, language)
    elif id_match and str(user_id) in DEV_array:
        await SearchId(update, id_match, chat_id, user_id, language)
    elif id_match:
        await SearchId(update, id_match, chat_id, user_id, language, False)
    elif text == "/localtime":
        msg = await updateMsg.reply_text(lg.get("local.localtime", language), reply_markup=lc.button())
        DoDataInsert().init(user_id, chat_id, msg.message_id)
    elif text == "/language":
        msg = await updateMsg.reply_text("local time", reply_markup=lg.button(language))
        DoDataInsert().init(user_id, chat_id, msg.message_id)
    elif updateMsg.chat.type == "private":
        await StartSet(update, text, user_id, chat_id, language)


async def DoCommands(update: Update, Data, ReplayText, ButtonMark, user_id, chat_id, lang):
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
        msg = await update.message.reply_text(lg.get(ReplayText, lang), reply_markup=ButtonMark)
        msgID = msg.message_id
        if ReplayText == 'delete.start':
            DoDataInsert().Del().init(user_id, chat_id, msgID)
        else:
            DoDataInsert().Redo().init(user_id, user_id, msgID)
    else:
        await update.message.reply_text(lg.get("both.none", lang))


async def SetSchedule(update: Update, checkCommands, text, user_id, chat_id, lang):
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
        await update.message.reply_text(lg.get("schedule.none.error", lang))
    else:
        await StartSet(update, clear_text, user_id, chat_id, lang)


async def StartSet(update: Update, text, user, chat, lang):
    """
    判斷是否過長並給出相對的詢問
    :param update:
    :param text: 使用者輸入之訊息
    :param user: 使用者id
    :param chat: 聊天頻道
    :param lang: 翻譯語言
    :return:
    """
    if len(text) <= MessageLen:
        msg = await update.message.reply_text(f"{lg.get('schedule.reminder.check.short', lang, text)}",
                                              reply_markup=true_false_text(lang))
    else:
        await update.message.reply_text(text)
        msg = await update.message.reply_text(text=lg.get('schedule.reminder.check.long', lang),
                                              reply_markup=true_false_text(lang))
    messageID = msg.message_id
    ScheduleStart(user, chat, messageID, text)


async def SearchId(update: Update, id_match, chat_id, user_id, lang: str, isDEV: bool = True):
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
    get_Need_Id = str(id_match.group(1))
    formatted_item = None
    long_item = None
    if isDEV:
        data = GetIdData(get_Need_Id)
    else:
        data = GetIdUserData(get_Need_Id, user_id, chat_id)
    for item in data:
        if not item:
            return
        item1 = str(item[1])
        if len(item1) <= 1800:
            formatted_item = (f"{lg.get('id.time', lang, item[2])} |"
                              f"{lg.get('id.short.reminder', lang, item[1])}")
        else:
            formatted_item = (f"{lg.get('id.time', lang, item[2])} |"
                              f"{lg.get('id.long.reminder', lang)}")
            long_item = item[1]
    if formatted_item is None:
        await update.message.reply_text(f"{lg.get('id.none', lang, get_Need_Id)}")
        return
    if long_item is None:
        await update.message.reply_text(f"{lg.get('id.get', lang, get_Need_Id)}\n{formatted_item}")
    else:
        await update.message.reply_text(f"{lg.get('id.get', lang, get_Need_Id)}\n{formatted_item}")
        await bot.send_message(chat_id, long_item)
