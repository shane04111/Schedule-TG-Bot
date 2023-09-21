from telegram import Bot
from function.SQL_Model import GetData
from dotenv import load_dotenv
import os
import asyncio


async def send():
    data = GetData()
    if not data.len():
        load_dotenv()
        TOKEN = os.getenv("TOKEN")
        bot = Bot(token=TOKEN)
        for index in GetData():
            await bot.sendMessage(index[1], index[0])


async def main():  # 将 main 函数也改成异步
    await send()  # 使用 await 来等待 send 函数完成


if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run 来运行异步代码
