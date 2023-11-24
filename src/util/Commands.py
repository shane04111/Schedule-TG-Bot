import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from src.function.ScheduleModel import sqlModel
from src.function.UserDataModel import DoDataInsert
from src.function.UserLocalModel import UserLocal
from src.function.loggr import logger
from src.function.my_time import time_datetime
from src.function.replay_markup import ShowButton
from src.local.localTime import Local
from src.translator.getLang import Language
from src.util import DEV_array

sql = sqlModel()


# TODO: user Local language and time
class commands:
    def __init__(self):
        self._lc = Local()
        self._lg = Language()
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
        userMsg = self._update.message_id
        msg = await self._update.reply_text(self._lg.get("local.group", self._language))
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id, userMsg)

    async def language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        userMsg = self._update.message_id
        msg = await self._update.reply_text("local time", reply_markup=self._lg.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id, userMsg)

    async def localTime(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        userMsg = self._update.message_id
        msg = await self._update.reply_text(
            self._lg.get("local.localtime", self._language),
            reply_markup=self._lc.button())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id, userMsg)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log the error and send a telegram message to notify the developer."""
        # Log the error before we do anything else, so we can see it even if something breaks.
        logger.error("Telegram error ", exc_info=context.error)
        sql.saveError(f"{time_datetime()} - ERROR - {context.error}", self._DEV_ID, self._DEV_ID)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self._init(update)
        await self._update.reply_text(self._lg.get("start", self._language))

    async def show(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        await self._showChange()

    async def showAll(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._init(update)
        if str(self._user_id) in DEV_array and str(self._chat_id) in DEV_array:
            await self._showChange(True)
            return
        else:
            await self._update.reply_text('無權限')

    async def _showChange(self, isAll: bool = False):
        button = ShowButton(1, self._user_id, self._chat_id, isAll, self._language)
        if button.final == 0:
            await self._update.reply_text(self._lg.get('schedule.show.none', self._language))
            return
        if isAll:
            data = sql.showAllData(0)
        else:
            data = sql.showData(self._user_id, self._chat_id, 0)
        replyText = button.showContext(data)
        userMsg = self._update.message_id
        msg = await self._update.reply_text(
            self._lg.get('schedule.show', self._language,
                         replyText, '1', str(button.number), str(button.final)),
            reply_markup=button.showButton())
        DoDataInsert().init(self._user_id, self._chat_id, msg.message_id, userMsg)
