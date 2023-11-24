import os

from dotenv import load_dotenv
from telegram import Bot

MessageLen = 3500
load_dotenv()
TOKEN = os.getenv('TOKEN')
DEV_ID = os.getenv('DEV')
DEV_array = [os.getenv("DEV"), os.getenv("DEV1")]
bot = Bot(token=TOKEN)
