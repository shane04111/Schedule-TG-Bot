import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.function.ScheduleModel import sqlModel
from src.function.UserDataModel import DoDataInsert
from src.function.UserLocalModel import UserLocal
from src.function.loggr import logger
from src.function.my_time import time_datetime, time_year, time_month, time_day, time_hour, time_minute, time_second
from src.function.replay_markup import showButton
from src.local.localTime import Local
from src.translator.getLang import Language

sql = sqlModel()


# TODO: user Local language and time
class commands:
    def __init__(self):
        self._lc = Local()
        self._lg = Language()
        self._user_id = None
        self._chat_id = None
        self._language = None
        self._update = None
        load_dotenv()
        self._DEV_ID = int(os.getenv("DEV"))

    def _init(self, update: Update):
        self._update = update.message
        self._user_id = self._update.from_user.id
        self._chat_id = self._update.chat.id
        local = UserLocal(self._chat_id)
        self._language = self._lg.getDefault(local, self._update.from_user.language_code)
        return self

    async def default(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await self._update.reply_text(self._lg.get("local.group", self._language))
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await self._update.reply_text("local time", reply_markup=self._lg.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def localTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        msg = await self._update.reply_text(
            self._lg.get("local.localtime", self._language),
            reply_markup=self._lc.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # todo 將資料庫轉移至 Schedule.Error
        # Log the error before we do anything else, so we can see it even if something breaks.
        logger.error("Telegram error ", exc_info=context.error)
        sql.saveError(f"{time_datetime()} - ERROR - {context.error}", self._DEV_ID, self._DEV_ID)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self._init(update)
        await self._update.reply_text(self._lg.get("start", self._language))

    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        button = showButton(1, self._user_id, self._chat_id)
        if button.final == 0:
            await self._update.reply_text(self._lg.get('schedule.show.none', self._language))
            return
        data = sql.showData(self._user_id, self._chat_id, 0)
        replyText = button.showContext(data)
        msg = await self._update.reply_text(
            self._lg.get('schedule.show', self._language,
                         replyText, '1', str(button.number), str(button.final)),
            reply_markup=button.showButton())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id)
