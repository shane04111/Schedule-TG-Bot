import logging
import os

import telegram.error
from dotenv import load_dotenv
from sqlite3 import Error
from telegram import Bot, Update
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from src.function.ScheduleModel import DBHandler, CheckFile
from src.function.loggr import logger, logFinal
from src.util.ButtonHandler import ScheduleButton
from src.util.MessageHandle import MessageHandle

logger.info('logger start')
DBHandler.connect()
load_dotenv()
TOKEN = os.getenv('TOKEN')
DEV_ID = os.getenv("DEV")
bot = Bot(token=TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("歡迎使用機器人！\n!s 創建一個新的提醒")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Telegram error ", exc_info=context.error)
    await bot.sendMessage(DEV_ID, f"TG機器人發生了神奇的錯誤：{context.error}")


def app():
    """
    機器人初始化
    :return:
    """
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CallbackQueryHandler(ScheduleButton))
    application.add_handler(MessageHandler(filters.TEXT, MessageHandle))

    print("機器人已上線")
    logger.info('機器人已上線')
    application.run_polling(poll_interval=1, allowed_updates=Update.ALL_TYPES)


def main():
    """
    程式入口
    :return:
    """
    CheckFile()
    app()


if __name__ == "__main__":
    try:
        main()
    except SyntaxError:
        logger.error('代碼寫錯了喔: ', exc_info=True)
    except NameError:
        logger.error('有個參數設定錯誤: ', exc_info=True)
    except telegram.error.NetworkError:
        logger.error('telegram 網路錯誤: ', exc_info=True)
    except telegram.error.TelegramError:
        logger.error('telegram API 錯誤: ', exc_info=True)
    except Error:
        logger.error('sqlite3錯誤: ', exc_info=True)
    except:
        logger.error('其他錯誤: ', exc_info=True)
    finally:
        DBHandler.Close()
        logger.info('logger end')
        logging.shutdown()
        logFinal()
