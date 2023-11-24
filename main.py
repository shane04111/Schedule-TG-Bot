import logging
import os

import telegram.error
from dotenv import load_dotenv
from sqlite3 import Error
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from src.function.loggr import logger, logFinal
from src.util.ButtonHandler import ScheduleButton
from src.util.Commands import commands
from src.util.MessageHandle import MessageHandle

logger.info('logger start')
load_dotenv()
TOKEN = os.getenv('TOKEN')
DEV_ID = os.getenv("DEV")
bot = Bot(token=TOKEN)


def app():
    """
    機器人初始化
    :return:
    """
    application = ApplicationBuilder().token(TOKEN).build()
    command = commands()

    application.add_error_handler(command.error_handler)
    application.add_handler(CommandHandler(["start", "help"], command.start))
    application.add_handler(CommandHandler("default", command.default))
    application.add_handler(CommandHandler("language", command.language))
    application.add_handler(CommandHandler("loacltime", command.localTime))
    application.add_handler(CommandHandler("show", command.show))
    application.add_handler(CommandHandler("showall", command.showAll))
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
        logger.info('logger end')
        logging.shutdown()
        logFinal()
