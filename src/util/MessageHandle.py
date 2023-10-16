import re

from telegram import Update
from telegram.ext import ContextTypes

from function import lg
from function.ScheduleModel import GetUserMessage, GetUserDoneMessage, GetIdData, GetIdUserData
from function.UserDataModel import ScheduleStart, DoDataInsert
from function.UserLocalModel import UserLocal
from function.deleteMessage import CreateDeleteButton, CreateRedoButton
from function.loggr import logger
from function.replay_markup import true_false_text
from util import MessageLen, DEV_ID, DEV_array, bot


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
    defaultLanguage = updateMsg.from_user.language_code
    if local.Check:
        language = local.Language
    elif defaultLanguage is None and defaultLanguage not in lg.lang and not local.Check:
        local.initUserLocal()
        language = "zh-hant"
    else:
        local.initUserLocal(defaultLanguage)
        language = defaultLanguage
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
    if text == "!id" and str(user_id) == DEV_ID:
        await updateMsg.reply_text(f"{updateMsg.message_id}")
    elif re.match(checkCommands, text):
        await SetSchedule(update, checkCommands, text, user_id, chat_id, language)
    elif re.match(deleteCommands, text):
        await DoCommands(update, DelData, "請選取要刪除的提醒訊息", CreateDeleteButton(user_id, chat_id),
                         user_id, chat_id)
    elif re.match(redoCommands, text):
        await DoCommands(update, RedoData, "請選擇要重新提醒的訊息", CreateRedoButton(user_id, chat_id),
                         user_id, chat_id)
    elif id_match and str(user_id) in DEV_array:
        await SearchId(update, id_match, chat_id, user_id)
    elif id_match:
        await SearchId(update, id_match, chat_id, user_id, False)
    elif updateMsg.chat.type == "private":
        await StartSet(update, text, user_id, chat_id)


async def DoCommands(update: Update, Data, ReplayText, ButtonMark, user_id, chat_id):
    """
    回復傳入訊息並根據傳入資料建立訊息之按鈕
    :param update:
    :param Data: 數據庫回膗資料
    :param ReplayText: 回復訊息
    :param ButtonMark: 建立按鈕
    :param user_id: 使用者id
    :param chat_id: 頻道id
    :return:
    """
    if Data:
        msg = await update.message.reply_text(ReplayText, reply_markup=ButtonMark)
        msgID = msg.message_id
        if ReplayText == '請選取要刪除的提醒訊息':
            DoDataInsert().Del().init(user_id, chat_id, msgID)
        else:
            DoDataInsert().Redo().init(user_id, user_id, msgID)
    else:
        await update.message.reply_text("尚未設定提醒")


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
        await StartSet(update, clear_text, user_id, chat_id)


async def StartSet(update: Update, text, user, chat):
    """
    判斷是否過長並給出相對的詢問
    :param update:
    :param text: 使用者輸入之訊息
    :param user: 使用者id
    :param chat: 聊天頻道
    :return:
    """
    if len(text) <= MessageLen:
        msg = await update.message.reply_text(f"請確認提醒事項：\n{text}", reply_markup=true_false_text)
    else:
        await update.message.reply_text(text)
        msg = await update.message.reply_text("是否提醒上述事項", reply_markup=true_false_text)
    messageID = msg.message_id
    ScheduleStart(user, chat, messageID, text)


async def SearchId(update: Update, id_match, chat_id, user_id, isDEV: bool = True):
    """
    尋找特定id訊息，並將提醒內容傳給使用者
    :param update:
    :param id_match: 使用者輸入指令
    :param chat_id: 頻道id
    :param user_id: 使用者id
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
        if item:
            item1 = str(item[1])
            if len(item1) <= 1800:
                formatted_item = f"提醒時間: {item[2]} |提醒事項: \n{item[1]}"
            else:
                formatted_item = f"提醒時間: {item[2]} |提醒事項: \n"
                long_item = f"{item[1]}"
    if formatted_item is None:
        await update.message.reply_text(f"ID {get_Need_Id} 不存在")
    else:
        if long_item is None:
            await update.message.reply_text(f"ID {get_Need_Id} 的資料是\n{formatted_item}")
        else:
            await update.message.reply_text(f"ID {get_Need_Id} 的資料是\n{formatted_item}")
            await bot.send_message(chat_id, long_item)
