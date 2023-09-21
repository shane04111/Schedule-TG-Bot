from telegram import Bot
from function.SQL_Model import GetData
import json
import asyncio

with open("config.json", "r") as f:
    config = json.load(f)
TOKEN = config["TOKEN"]

bot = Bot(token=TOKEN)


async def send():
    # 棄用
    # 改用SQL lite
    # with open('data/schedule.json', 'r') as file:
    #     schedule_json_data = json.load(file)
    # schedule_list = schedule_json_data["schedule"]
    # for index, data in enumerate(schedule_list):
    #     user_message = data["text"]
    #     user_chat_id = data["chat_id"]
    #     user_year = data["year"]
    #     user_month = data["month"]
    #     user_day = data["day"]
    #     user_hour = data["hour"]
    #     user_minute = data["minute"]
    #     now_time = f"{time_year()}/{time_month()}/{time_day()}-{time_hour()}:{time_minute()}"
    #     user_time = f"{user_year}/{user_month}/{user_day}-{user_hour}:{user_minute}"
    #     if now_time == user_time:
    #         await bot.sendMessage(user_chat_id, user_message)
    for index in GetData():
        await bot.sendMessage(index[1], index[0])


async def main():  # 将 main 函数也改成异步
    await send()  # 使用 await 来等待 send 函数完成


if __name__ == "__main__":
    asyncio.run(main())  # 使用 asyncio.run 来运行异步代码
