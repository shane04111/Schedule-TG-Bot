from telegram import Bot
from src.function.SendSqlModel import GetData, getError, change
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)


async def send(data: list[tuple], table: int):
    for index in data:
        msg = await bot.sendMessage(index[1], index[0])
        if msg:
            change(index[2], table)
        else:
            print(f"ID: {index[2]} 訊息發送失敗")
            return


async def main():
    """
    程式開始入口 \n
    從資料庫抓取比當前時間早並且尚未提醒過的訊息，並且發送給使用者
    :return:
    """
    errorData = getError()
    data = GetData()
    await send(errorData, 1)
    await send(data, 2)


if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run 来运行异步代码
