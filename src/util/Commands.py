import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.function.ScheduleModel import SqlModel
from src.function.UserDataModel import start
from src.function.UserLocalModel import UserLocal
from src.function.logger import logger
from src.function.my_time import myTime
from src.function.replay_markup import ShowButton
from src.local.localTime import Local
from src.translator.getLang import Language
from src.util import DEV_array

sql = SqlModel()


class Commands:
    def __init__(self):
        self._lc = Local()
        self._lg = Language()
        load_dotenv()
        self._DEV_ID = int(os.getenv("DEV"))

    def _init(self, update: Update):
        self._update = update.message
        if not self._update:
            self._update = None
            self._initEdit(update)
            return self
        self._initial()
        return self

    def _initEdit(self, update: Update):
        self._update = update.edited_message
        self._initial()
        edit_data = sql.getMessageID(self._chat_id, self._message_id)
        if len(edit_data) > 1:
            logger.error(
                f'預期只有一筆資料，但回傳了 {len(edit_data)} 筆資料\ndata: {edit_data}\nFile: "{__file__}", line 42')
            return
        self._edit_message_id = edit_data[0][0]
        self._edit_id = edit_data[0][1]

    def _initial(self):
        self._user_id = self._update.from_user.id
        self._chat_id = self._update.chat.id
        self._message_id = self._update.message_id
        local = UserLocal(self._chat_id, self._user_id)
        self._language = self._lg.getDefault(local, self._update.from_user.language_code)

    async def default(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        await self._send(update, context, self._lg.get("local.group", self._language))
        return

    async def language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        await self._send(update, context, "local time", self._lg.button())
        return

    async def localTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        await self._send(update, context, self._lg.get("local.localtime", self._language), self._lc.button())
        return

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        update.__dir__()
        logger.error("Telegram error ", exc_info=context.error)
        sql.saveError(f"{myTime().now} - ERROR - {context.error}", self._DEV_ID, self._DEV_ID)
        return

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self._init(update)
        await self._send(update, context, self._lg.get("start", self._language))
        return

    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        await self._showChange(update, context)
        return

    async def showAll(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        if str(self._user_id) in DEV_array and str(self._chat_id) in DEV_array:
            await self._showChange(update, context, True)
            return
        else:
            await self._send(update, context, '無權限')
            return

    async def _showChange(self, update: Update, context: ContextTypes.DEFAULT_TYPE, isAll: bool = False):
        button = ShowButton(1, self._user_id, self._chat_id, isAll, self._language)
        if button.final == 0:
            await self._update.reply_text(self._lg.get('schedule.show.none', self._language))
            return
        if isAll:
            data = sql.showAllData(0)
        else:
            data = sql.showData(self._user_id, self._chat_id, 0)
        reply_text = button.showContext(data)
        await self._send(update, context,
                         self._lg.get('schedule.show', self._language,
                                      reply_text, '1', str(button.number), str(button.final)),
                         button.showButton())

    async def _send(self, update: Update,
                    context: ContextTypes.DEFAULT_TYPE,
                    text: str,
                    mark: InlineKeyboardMarkup | None = None) -> None:
        """
        將斜線指令的回覆改為回復或編輯
        :param update: 預設的第一個參數
        :param context: 預設的第兩個參數
        :param text: 訊息
        :param mark: 按鈕
        :return:
        """
        if self._update is update.edited_message:
            await context.bot.edit_message_text(text, self._chat_id, self._edit_message_id, reply_markup=mark)
            return
        msg = await self._update.reply_text(text, reply_markup=mark)
        start(self._user_id, self._chat_id, msg.message_id, self._message_id, self._update.text)
        return
