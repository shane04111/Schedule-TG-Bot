import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from src.function.ScheduleModel import DBHandler
from src.function.UserDataModel import DoDataInsert
from src.function.UserLocalModel import UserLocal
from src.function.loggr import logger
from src.function.my_time import time_datetime
from src.local.localTime import Local
from src.translator.getLang import Language


# TODO: user Local language and time
class commands:
    def __init__(self):
        self.lc = Local()
        self.lg = Language()
        self._user_id = None
        self._chat_id = None
        self._language = None
        load_dotenv()
        self.DEV_ID = os.getenv("DEV")

    def _init(self, update):
        self._user_id = update.message.from_user.id
        self._chat_id = update.message.chat.id
        local = UserLocal(self._chat_id)
        self._language = self.lg.getDefault(local, update.message.from_user.language_code)
        return self

    async def default(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await update.message.reply_text(self.lg.get("local.group", self._language))
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await update.message.reply_text("local time", reply_markup=self.lg.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def localTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await update.message.reply_text(
            self.lg.get("local.localtime", self._language),
            reply_markup=self.lc.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        logger.error("Telegram error ", exc_info=context.error)
        DBHandler.insertData(
            'Schedule.schedule', ('Message', 'UserID', 'ChatID', 'DateTime', 'UserTime'),
            (f"{time_datetime()} - ERROR - {context.error}",
             self.DEV_ID, self.DEV_ID, time_datetime(), time_datetime()))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self._init(update)
        await update.message.reply_text(self.lg.get("歡迎使用機器人！\n!s 創建一個新的提醒", self._language))
