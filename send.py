from telegram import Bot
from function.ScheduleModel import GetData, ChangeSendTrue, DBHandler
from dotenv import load_dotenv
import os
import asyncio

DBHandler.sendConnect()
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


async def main():
    """
    程式開始入口 \n
    從資料庫抓取比當前時間早並且尚未提醒過的訊息，並且發送給使用者
    :return:
    """
    data = GetData()
    for index in data:
        await bot.sendMessage(index[1], index[0])
        ChangeSendTrue(str(index[2]))

asyncio.run(main())  # 使用 asyncio.run 来运行异步代码
