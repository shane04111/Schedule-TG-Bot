from telegram import Bot
from function.SQL_Model import GetData, ChangeSend
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


async def send():
    data = GetData()
    for index in data:
        await bot.sendMessage(index[1], index[0])
        ChangeSend(str(index[2]))


if __name__ == "__main__":
    asyncio.run(send())  # 使用 asyncio.run 来运行异步代码
