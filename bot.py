from telegram import Update, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from function.replay_markup import true_false_text, time_chose_data_function, TD_check, SD_check, OY_check, \
    ALL_check, HR_check, MIN_check, config_check, day_check, check_YMD, month_check, year_check
from function.my_time import time_year, time_month, time_day, time_hour, time_minute
from function.hour_select import hour_select, convert_to_chinese_time
from function.minute_select import minute_select, check_minute_time
from function.day_select import day_select
from function.month_select import month_select
from function.year_select import year_select
from function.SQL_Model import SaveData, CheckFile, GetData
import json
import threading
import re

with open("config.json", "r") as f:
    config = json.load(f)
TOKEN = config["TOKEN"]

bot = Bot(token=TOKEN)

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("歡迎使用機器人！\n/schedule 創建一個新的提醒")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    if re.match(r"^/schedule(@EZMinder_bot)?", text):
        clear_text = re.sub(r"^/schedule(@EZMinder_bot)?", "", text).strip()
        if clear_text == "":
            await update.message.reply_text("請重新使用 /schedule 並在後面加上提醒事項")
        else:
            user_data[f"{user_id}|{chat_id}"] = {
                "text": clear_text,
                "user_id": user_id,
                "chat_id": chat_id
            }

            await update.message.reply_text(f"請確認提醒事項：{clear_text}", reply_markup=true_false_text)
    elif re.match(r"^/s(@EZMinder_bot)?", text):
        clear_text = re.sub(r"/s((@EZMinder_bot)?)", "", text).strip()
        if clear_text == "":
            await update.message.reply_text("請重新使用 /s 並在後面加上提醒事項")
        else:
            user_data[f"{user_id}|{chat_id}"] = {
                "text": clear_text,
                "user_id": user_id,
                "chat_id": chat_id
            }

            await update.message.reply_text(f"請確認提醒事項：{clear_text}", reply_markup=true_false_text)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global get_need_data
    query = update.callback_query
    query_user_id = update.callback_query.from_user.id
    query_chat_id = update.callback_query.message.chat.id
    # ==========user_data===========
    query_get_key = f"{query_user_id}|{query_chat_id}"
    get_need_data = None
    if query_get_key in user_data:
        get_need_data = user_data[query_get_key]
    else:
        await bot.sendMessage(query_chat_id, "按鈕已過時或無權限")
    # ===========match==============
    day_match = re.search(r'(\d+)day', query.data)
    hour_match = re.search(r'(\d+)hour', query.data)
    min_match = re.search(r'(\d+)min', query.data)
    month_match = re.search(r'(\d+)month', query.data)
    year_match = re.search(r'(\d+)year', query.data)
    await query.answer()
    if query_get_key in user_data and get_need_data.get('user_id') == query_user_id:
        if query.data == "text_true":
            await query.edit_message_text(text="請選擇提醒時間", reply_markup=time_chose_data_function())
        elif query.data == "text_false":
            user_data.pop(query_get_key)
            await query.edit_message_text(text="結束提醒設定\n如需設定其他提醒請重新使用 /schedule")
        elif query.data == "today":
            get_need_data.update({
                "year": time_year(),
                "month": time_month(),
                "day": time_day(),
                "is_today": True,
                "isOY": False
            })
            await query.edit_message_text(f"確認選擇將日期設定為{time_year()}/{time_month()}/{time_day()}",
                                          reply_markup=TD_check)
        elif query.data == "set_day":
            get_need_data.update({
                "year": check_YMD().year,
                "month": check_YMD().month,
                "day": "",
                "is_today": False,
                "isOY": False
            })
            await query.edit_message_text(f"確認選擇將日期設定為{check_YMD().year}/{check_YMD().month}",
                                          reply_markup=SD_check)
        elif query.data == "only_year":
            get_need_data.update({
                "year": check_YMD().year,
                "month": "",
                "day": "",
                "is_today": False,
                "isOY": True
            })
            await query.edit_message_text(f"確認選擇將日期設定為{check_YMD().year}", reply_markup=OY_check)
        elif query.data == "all_set":
            get_need_data.update({
                "year": "",
                "month": "",
                "day": "",
                "is_today": False,
                "isOY": True
            })
            await query.edit_message_text("確認自訂義日期", reply_markup=ALL_check)
        elif query.data in ["ALL_false", "TD_false", "OY_false", "SD_false", "month_back", "year_back"]:
            await query.edit_message_text("請選擇提醒時間", reply_markup=time_chose_data_function())
        elif query.data == "ALL_true":
            await query.edit_message_text("請選擇要幾年提醒", reply_markup=year_select(time_year() + 1))
        elif year_match:
            get_year = int(year_match.group(1))
            get_need_data["year"] = get_year
            await query.edit_message_text(f"確認選擇{get_year}年提醒", reply_markup=year_check)
        elif query.data == "year_true":
            await query.edit_message_text("請選擇要幾月提醒", reply_markup=month_select(1))
        elif query.data == "year_false":
            await query.edit_message_text("請選擇要幾年提醒", reply_markup=year_select(time_year() + 1))
        elif query.data == "OY_true":
            if check_YMD().is_valid:
                month_need = check_YMD().month
            else:
                month_need = time_month() + 1
            await query.edit_message_text("請選擇要幾月提醒", reply_markup=month_select(month_need))
        elif month_match:
            get_month = int(month_match.group(1))
            get_need_data["month"] = get_month
            await query.edit_message_text(f"確認選擇{get_month}月提醒", reply_markup=month_check)
        elif query.data == "month_true":
            year_need = get_need_data["year"]
            month_need = get_need_data["month"]
            await query.edit_message_text("請選擇要幾號提醒", reply_markup=day_select(year_need, month_need, 1))
        elif query.data == "month_false":
            if time_year() == get_need_data["year"]:
                if check_YMD().is_valid:
                    month_need = check_YMD().month
                else:
                    month_need = time_month() + 1
            else:
                month_need = 1
            await query.edit_message_text("請選擇要幾月提醒", reply_markup=month_select(month_need))
        elif query.data == "SD_true":
            if check_YMD().is_valid:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = 1
            else:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = time_day() + 1
            await query.edit_message_text("請選擇要幾號提醒", reply_markup=day_select(year_need, month_need, day_need))
        elif day_match:
            get_day = int(day_match.group(1))
            get_need_data["day"] = get_day
            await query.edit_message_text(f"確認選擇{get_day}號提醒", reply_markup=day_check)
        elif query.data == "day_back":
            if get_need_data["isOY"]:
                if time_year() == get_need_data["year"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                    else:
                        month_need = time_month() + 1
                else:
                    month_need = 1
                await query.edit_message_text("請選擇要幾月提醒", reply_markup=month_select(month_need))
            else:
                await query.edit_message_text("請選擇提醒時間", reply_markup=time_chose_data_function())
        elif query.data == "day_true":
            await query.edit_message_text("請選擇要幾點提醒", reply_markup=InlineKeyboardMarkup(hour_select(0)))
        elif query.data == "day_false":
            if time_year() == get_need_data["year"] and time_month == get_need_data["month"]:
                year_need = time_year()
                month_need = time_month()
                day_need = time_day() + 1
            else:
                year_need = get_need_data["year"]
                month_need = get_need_data["month"]
                day_need = 1
            await query.edit_message_text("請選擇要幾號提醒", reply_markup=day_select(year_need, month_need, day_need))
        elif query.data == "TD_true":
            if time_minute() > 57:
                set_select_hour = time_hour() + 1
            else:
                set_select_hour = time_hour()
            await query.edit_message_text("請選擇要幾點提醒",
                                          reply_markup=InlineKeyboardMarkup(hour_select(set_select_hour)))
        elif hour_match:
            get_hour = int(hour_match.group(1))
            get_need_data["hour"] = get_hour
            await query.edit_message_text(f"確認選擇{convert_to_chinese_time(get_hour)}", reply_markup=HR_check)
        elif query.data == "HR_true":
            await query.edit_message_text("請選擇要幾分提醒", reply_markup=hour_check_button(query_get_key))
        elif query.data == "HR_false":
            await query.edit_message_text("請選擇要幾點提醒", reply_markup=InlineKeyboardMarkup(
                hour_select(hour_check_need(query_get_key))))
        elif query.data == "HR_back":
            if get_need_data["is_today"]:
                await query.edit_message_text(text="請選擇提醒時間", reply_markup=time_chose_data_function())
            else:
                if time_year() == get_need_data["year"] and time_month() == get_need_data["month"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                        day_need = 1
                    else:
                        month_need = check_YMD().month
                        day_need = time_day() + 1
                    await query.edit_message_text("請選擇要幾號提醒",
                                                  reply_markup=day_select(time_year(), month_need, day_need))
                else:
                    await query.edit_message_text("請選擇要幾號提醒",
                                                  reply_markup=day_select(get_need_data["year"], get_need_data["month"],
                                                                          1))
        elif min_match:
            get_min = int(min_match.group(1))
            get_need_data["minute"] = get_min
            await query.edit_message_text(f"確認選擇{check_minute_time(get_min)}", reply_markup=MIN_check)
        elif query.data == "MIN_true":
            await query.edit_message_text(message_check_text(get_need_data), reply_markup=config_check)
        elif query.data == "MIN_false":
            await query.edit_message_text("請選擇要幾分提醒", reply_markup=hour_check_button(query_get_key))
        elif query.data == "MIN_back":
            await query.edit_message_text("請選擇要幾點提醒", reply_markup=InlineKeyboardMarkup(
                hour_select(hour_check_need(query_get_key))))
        elif query.data == "config_true":
            # 棄用
            # 將儲存方式由json轉至SQL lite
            # with open("data/schedule.json", "r") as json_file:
            #     schedule_data = json.load(json_file)
            # schedule_data["schedule"].append(get_need_data)
            # with open("data/schedule.json", "w") as json_file:
            #     json.dump(schedule_data, json_file)
            text = get_need_data["text"]
            chatid = get_need_data["chat_id"]
            user_year = get_need_data["year"]
            user_month = get_need_data["month"]
            user_day = get_need_data["day"]
            user_hour = get_need_data["hour"]
            user_minute = get_need_data["minute"]
            SaveData(text, chatid, user_year, user_month, user_day, user_hour, user_minute)
            user_data.pop(query_get_key)
            await query.edit_message_text("已成功安排提醒\n如需設定其他提醒請再次輸入 /schedule")
        elif query.data == "config_false":
            await query.edit_message_text(text="請選擇提醒時間", reply_markup=time_chose_data_function())
        elif query.data == "config_cancel":
            user_data.pop(query_get_key)
            await query.edit_message_text("已取消安排提醒\n如需設定其他提醒請再次輸入 /schedule")
    else:
        return


def message_check_text(get_need_data):
    edit_message = f"是否選擇{get_need_data['year']}/{str(get_need_data['month']).zfill(2)}/{str(get_need_data['day']).zfill(2)} \
        \n{convert_to_chinese_time(get_need_data['hour'])}{minute_to_chinese(get_need_data['minute'])}提醒\n提醒事項：{get_need_data['text']}"
    return edit_message


def minute_to_chinese(minute):
    if minute == 0:
        return "整"
    if 0 < minute < 10:
        return f"0{minute}分"
    else:
        return f"{minute}分"


def hour_check_button(user_data_key):
    if user_data[user_data_key]["is_today"]:
        if user_data[user_data_key]["hour"] == time_hour():
            set_minute_button = InlineKeyboardMarkup(minute_select(True))
            return set_minute_button
        else:
            set_minute_button = InlineKeyboardMarkup(minute_select(False))
            return set_minute_button
    else:
        set_minute_button = InlineKeyboardMarkup(minute_select(False))
        return set_minute_button


def hour_check_need(user_data_key):
    if user_data[user_data_key]["is_today"]:
        if time_minute() > 57:
            set_select_hour = time_hour() + 1
            return set_select_hour
        else:
            set_select_hour = time_hour()
            return set_select_hour
    else:
        set_select_hour = 0
        return set_select_hour


# 棄用
# async def job_to_do():
#     global stop
#     while True:
#         if time_second() == 0:
#             indices_del = []
#             with open('data/schedule.json', 'r') as file:
#                 schedule_json_data = json.load(file)
#             schedule_list = schedule_json_data["schedule"]
#             for index, data in enumerate(schedule_list):
#                 user_message = data["text"]
#                 user_chat_id = data["chat_id"]
#                 user_year = data["year"]
#                 user_month = data["month"]
#                 user_day = data["day"]
#                 user_hour = data["hour"]
#                 user_minute = data["minute"]
#                 now_time = f"{time_year()}/{time_month()}/{time_day()}-{time_hour()}:{time_minute()}"
#                 user_time = f"{user_year}/{user_month}/{user_day}-{user_hour}:{user_minute}"
#                 if now_time == user_time:
#                     await bot.sendMessage(user_chat_id, user_message)
#                     indices_del.append(index)
#                 if now_time > user_time:
#                     indices_del.append(index)
#             for index in reversed(indices_del):
#                 del schedule_list[index]
#                 with open('data/schedule.json', 'w') as del_file:
#                     json.dump(schedule_json_data, del_file, indent=2)
#         await asyncio.sleep(1)
#         if stop:
#             break


# 棄用
# def run_job_thread():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(job_to_do())
#     asyncio.run(job_to_do())
stop = False


def check():
    global stop
    while True:
        need_get = input("請輸入需要讀取的資料\n")
        if need_get == "user":
            print("user_data", json.dumps(user_data, indent=2))
        elif need_get == "database":
            with open("data/schedule.json", "r") as json_file:
                schedule_data = json.load(json_file)
            print(json.dumps(schedule_data, indent=2))
        elif need_get == "stop":
            break
        else:
            print("無法讀取\n可輸入：user以及database")
        if stop:
            break


def app():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.COMMAND, handle_message))

    print("機器人已上線")
    application.run_polling()


def main():
    global stop
    try:
        # 已棄用，轉移至 send.py 並使用排成工具每分鐘自動運行
        # threading.Thread(target=run_job_thread, daemon=True).start()
        threading.Thread(target=check, daemon=True).start()
        CheckFile()
        GetData()
        app()
    except KeyboardInterrupt:
        stop = True


if __name__ == "__main__":
    main()
