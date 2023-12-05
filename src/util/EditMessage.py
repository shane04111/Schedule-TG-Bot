import telegram
from telegram import Update
from telegram.ext import ContextTypes

from src.function import lg
from src.function.ScheduleModel import SqlModel
from src.function.UserLocalModel import UserLocal
from src.function.loggr import logger
from src.function.replay_markup import MarkUp
from src.util import MessageLen

sql = SqlModel()


async def editMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: 添加其他!指令
    edit_msg = update.edited_message
    if not edit_msg:
        return
    chat_id = edit_msg.chat.id
    user_id = edit_msg.from_user.id
    message_id = edit_msg.message_id
    local = UserLocal(chat_id, user_id)
    language = lg.getDefault(local, edit_msg.from_user.language_code)
    text = edit_msg.text
    edit_data = sql.getMessageID(chat_id, message_id)
    if len(edit_data) != 1:
        logger.error(f'預期只有一筆資料，但回傳了 {len(edit_data)} 筆資料\ndata: {edit_data}\nFile: "{__file__}", line 24')
        return
    edit_message_id = edit_data[0][0]
    edit_id = edit_data[0][1]
    if edit_msg.chat.type == "private":
        await _editMessage(context, text, chat_id, edit_message_id, edit_id, language)


async def _editMessage(context, text: str, chat: int, message: int, editID: int, lang: str):
    mark = MarkUp(lang)
    final = f"{text[:3500]}{'...' if len(text) > MessageLen else ''}"
    try:
        await context.bot.edit_message_text(
            lg.get('schedule.reminder.check.short', lang, final), chat, message, reply_markup=mark.firstCheck())
    except telegram.error.BadRequest:
        logger.debug(f'機器人嘗試編輯訊息錯誤\nat {__file__}, line 39')
        return
    sql.editText(editID, text)
