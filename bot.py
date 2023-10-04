import re
import telegram.error

from telegram import *
from telegram.ext import *
from function.SQL_Model import *
from function.day_select import day_select
from function.deleteMessage import CreateDeleteButton, CreateRedoButton
from function.hour_select import hour_select, convert_to_chinese_time
from function.minute_select import minute_select
from function.month_select import month_select
from function.my_time import *
from function.replay_markup import *
from function.year_select import year_select
from function.loggr import *

load_dotenv()
TOKEN = os.getenv("TOKEN")
DEV_ID = os.getenv("DEV")
bot = Bot(token=TOKEN)
logger = logInFile()
logger.info('logger start')

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("歡迎使用機器人！\n!s 創建一個新的提醒")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    檢測使用者輸入訊息，並詢問是否需要提醒
    :param update:
    :param context:
    :return:
    """
    text = None
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    if update.message and update.message.text:
        text = update.message.text
    else:
        logger.warning(f"消息為空或無文本內容, user:{user_id}, chat:{chat_id}")
    DelData = GetUserMessage(user_id, chat_id)
    RedoData = GetUserDoneMessage(user_id, chat_id)
    id_match = re.search(r'(\d+)([iI][dD])', text)
    checkCommands = r"(![sS]|/[sS])(chedule)?(@EZMinder_bot)?"
    deleteCommands = r"(![dD]|/[dD])(elete)?(@EZMinder_bot)?"
    redoCommands = r"(![rR]|/[rR])(edo)?(@EZMinder_bot)?"
    if re.match(checkCommands, text):
        await SetSchedule(update, checkCommands, text, user_id, chat_id)
    elif text == "!id":
        await update.message.reply_text(f"{update.message.message_id}")
    elif re.match(deleteCommands, text):
        await DoCommands(update, DelData, "請選取要刪除的提醒訊息", CreateDeleteButton(user_id, chat_id),
                         user_id, chat_id)
    elif re.match(redoCommands, text):
        await DoCommands(update, RedoData, "請選擇要重新提醒的訊息", CreateRedoButton(user_id, chat_id),
                         user_id, chat_id)
    elif id_match:
        await SearchId(update, id_match, chat_id)
    elif update.message.chat.type == "private":
        await StartSet(update, text, user_id, chat_id)


async def DoCommands(update, Data, ReplayText, ButtonMark, user_id, chat_id):
    """
    回復傳入訊息並根據傳入資料建立訊息之按鈕
    :param update:
    :param Data: 數據庫回膗資料
    :param ReplayText: 回復訊息
    :param ButtonMark: 建立按鈕
    :param user_id: 使用者id
    :param chat_id: 頻道id
    :return:
    """
    if Data:
        msg = await update.message.reply_text(ReplayText, reply_markup=ButtonMark)
        msgID = msg.message_id
        user_data[f"{user_id}|{chat_id}|{msgID}"] = {"user_id": user_id}
    else:
        await update.message.reply_text("尚未設定提醒")


async def SetSchedule(update, checkCommands, text, user_id, chat_id):
    """
    設定提醒事項
    :param update:
    :param checkCommands: 提醒前墜或指令
    :param text: 使用者輸入訊息
    :param user_id: 使用者id
    :param chat_id: 頻道id
    :return:
    """
    clear_text = re.sub(checkCommands, "", text).strip()
    if clear_text == "":
        await update.message.reply_text("請重新使用命令並在後面加上提醒事項")
    else:
        await StartSet(update, clear_text, user_id, chat_id)


async def StartSet(update, text, user, chat):
    """
    判斷是否過長並給出相對的詢問
    :param update:
    :param text: 使用者輸入之訊息
    :param user: 使用者id
    :param chat: 聊天頻道
    :return:
    """
    if len(text) <= 1900:
        msg = await update.message.reply_text(f"請確認提醒事項：{text}", reply_markup=true_false_text)
    else:
        await update.message.reply_text(text)
        msg = await update.message.reply_text("是否提醒上述事項", reply_markup=true_false_text)
    messageID = msg.message_id
    user_data[f"{user}|{chat}|{messageID}"] = {
        "text": text,
        "user_id": user,
        "chat_id": chat,
        "message_id": messageID
    }


async def SearchId(update, id_match, chat_id):
    """
    尋找特定id訊息，並將提醒內容傳給使用者
    :param update:
    :param id_match: 使用者輸入指令
    :param chat_id: 頻道id
    :return:
    """
    get_Need_Id = str(id_match.group(1))
    formatted_item = None
    long_item = None
    for item in GetIdData(get_Need_Id):
        if item:
            item1 = str(item[1])
            if len(item1) <= 1800:
                formatted_item = f"提醒時間: {item[2]} |提醒事項: \n{item[1]}"
            else:
                formatted_item = f"提醒時間: {item[2]} |提醒事項: \n"
                long_item = f"{item[1]}"
    if formatted_item is None:
        await update.message.reply_text(f"ID {get_Need_Id} 不存在")
    else:
        if long_item is None:
            await update.message.reply_text(f"ID {get_Need_Id} 的資料是\n{formatted_item}")
        else:
            await update.message.reply_text(f"ID {get_Need_Id} 的資料是\n{formatted_item}")
            await bot.send_message(chat_id, long_item)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    按鈕檢測及回應
    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    query_user_id = query.from_user.id
    query_chat_id = query.message.chat.id
    query_message_id = query.message.message_id
    # ==========user_data===========
    query_get_key = f"{query_user_id}|{query_chat_id}|{query_message_id}"
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
    delete_match = re.search(r'(\d+)del', query.data)
    await query.answer()
    if query_get_key in user_data and get_need_data.get('user_id') == query_user_id and get_need_data is not None:
        if query.data == "text_true":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "text_false":
            user_data.pop(query_get_key)
            await EditMessage(query, "結束提醒設定\n如需設定其他提醒請重新使用 /schedule")
        elif query.data == "time_back":
            text = get_need_data["text"]
            if len(text) <= 1900:
                await EditMessage(query, f"請確認提醒事項：{text}", true_false_text)
            else:
                await EditMessage(query, "是否提醒上述事項", true_false_text)
        elif query.data == "today":
            SaveTimeDate(get_need_data, time_year(), time_month(), time_day(), True, False)
            if time_minute() > 57:
                set_select_hour = time_hour() + 1
            else:
                set_select_hour = time_hour()
            await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾點提醒",
                              hour_select(set_select_hour))
        elif query.data == "set_day":
            SaveTimeDate(get_need_data, check_YMD().year, check_YMD().month, "", False, False)
            if check_YMD().is_valid:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = 1
            else:
                year_need = check_YMD().year
                month_need = check_YMD().month
                day_need = time_day() + 1
            await EditMessage(query, f"{SendTime(get_need_data, 2)}\n請選擇要幾號提醒",
                              day_select(year_need, month_need, day_need))
        elif query.data == "only_year":
            SaveTimeDate(get_need_data, check_YMD().year, "", "", False, True)
            if check_YMD().is_valid:
                month_need = check_YMD().month
            else:
                month_need = time_month() + 1
            await EditMessage(query, f"{SendTime(get_need_data, 1)}\n請選擇要幾月提醒",
                              month_select(month_need))
        elif query.data == "all_set":
            SaveTimeDate(get_need_data, check_YMD().year, check_YMD().month, "", False, True)
            await EditMessage(query, "請選擇要幾年提醒", year_select(time_year() + 1))
        elif query.data == "year_back":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "month_back":
            year_need = get_need_data["year"]
            if year_need == time_year():
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
            else:
                await EditMessage(query, f"{SendTime(get_need_data, 1)}\n請選擇要幾年提醒",
                                  year_select(time_year() + 1))
        elif year_match:
            get_year = int(year_match.group(1))
            get_need_data["year"] = get_year
            await EditMessage(query, f"當前選擇時間 {get_year}\n請選擇要幾月提醒", month_select(1))
        elif month_match:
            get_month = int(month_match.group(1))
            get_need_data["month"] = get_month
            year_need = get_need_data["year"]
            await EditMessage(query, f"當前選擇時間 {year_need}/{get_month}\n請選擇要幾號提醒",
                              day_select(year_need, get_month, 1))
        elif day_match:
            get_day = int(day_match.group(1))
            get_need_data["day"] = get_day
            await EditMessage(query, f"{SendTime(get_need_data, 3)}",
                              hour_select(0))
        elif query.data == "day_back":
            if get_need_data["isOY"]:
                if time_year() == get_need_data["year"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                    else:
                        month_need = time_month() + 1
                else:
                    month_need = 1
                await EditMessage(query, f"{SendTime(get_need_data, 2)}\n請選擇要幾月提醒",
                                  month_select(month_need))
            else:
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif hour_match:
            get_hour = int(hour_match.group(1))
            get_need_data["hour"] = get_hour
            await EditMessage(query,
                              f"{SendTime(get_need_data, 4)}\n請選擇要幾分提醒",
                              hour_check_button(get_need_data))
        elif query.data == "HR_back":
            if get_need_data["is_today"]:
                await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
            else:
                if time_year() == get_need_data["year"] and time_month() == get_need_data["month"]:
                    if check_YMD().is_valid:
                        month_need = check_YMD().month
                        day_need = 1
                    else:
                        month_need = check_YMD().month
                        day_need = time_day() + 1
                    await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾號提醒",
                                      day_select(time_year(), month_need, day_need))
                else:
                    await EditMessage(query, f"{SendTime(get_need_data, 3)}\n請選擇要幾號提醒",
                                      day_select(get_need_data["year"], get_need_data["month"],
                                                 1))
        elif min_match:
            get_min = int(min_match.group(1))
            get_need_data["minute"] = get_min
            await EditMessage(query, message_check_text(get_need_data), config_check)
        elif query.data == "MIN_back":
            await EditMessage(query, f"{SendTime(get_need_data, 4)}\n請選擇要幾點提醒",
                              hour_select(hour_check_need(get_need_data)))
        elif query.data == "config_true":
            FinalSaveData(get_need_data)
            user_data.pop(query_get_key)
            await EditMessage(query, "已成功安排提醒\n如需設定其他提醒請再次輸入 /schedule")
        elif query.data == "config_false":
            await EditMessage(query, "請選擇提醒時間", time_chose_data_function())
        elif query.data == "config_back":
            await EditMessage(query, f"{SendTime(get_need_data, 4)}\n請選擇要幾分提醒",
                              hour_check_button(get_need_data))
        elif query.data == "cancel":
            user_data.pop(query_get_key)
            await EditMessage(query, "已取消安排提醒\n如需設定其他提醒請再次輸入 /schedule")
        elif delete_match:
            get_delete = str(delete_match.group(1))
            ChangeSendTrue(get_delete)
            DelData = GetUserMessage(query_user_id, query_chat_id)
            if DelData:
                await EditMessage(query, "已刪除所選提醒，還有以下提醒：",
                                  CreateDeleteButton(query_user_id, query_chat_id))
            else:
                await EditMessage(query, "無提醒訊息")
        elif query.data == "del":
            await EditMessage(query, "如需重新刪除提醒請再次輸入指令")
        else:
            logger.warning(f"錯誤的按鈕回傳: {query.data}")
            return
    else:
        return


async def EditMessage(query, editMessage, mark=None):
    try:
        await query.edit_message_text(editMessage, reply_markup=mark)
    except telegram.error.TelegramError:
        logger.warning('bot edit message error ', exc_info=True)
        return
    except:
        logger.error('else error ', exc_info=True)
        return


def FinalSaveData(data):
    """
    將使用者輸入的資料讀取出來並且存入資料庫
    :param data: 使用者資料
    :return:
    """
    text = data["text"]
    userID = data["user_id"]
    chatid = data["chat_id"]
    user_year = data["year"]
    user_month = data["month"]
    user_day = data["day"]
    user_hour = data["hour"]
    user_minute = data["minute"]
    SaveData(text, userID, chatid, "%04d" % user_year, "%02d" % user_month, "%02d" % user_day,
             "%02d" % user_hour, "%02d" % user_minute)


def SendTime(data, nowSet: int):
    """
    回傳當前設定時間
    :param data:
    :param nowSet:
    :return:
    """
    year = data["year"]
    match nowSet:
        case 1:
            return f"當前選擇時間 {year}"
        case 2:
            month = data["month"]
            return f"當前選擇時間 {year}/{month}"
        case 3:
            month = data["month"]
            day = data["day"]
            return f"當前選擇時間 {year}/{month}/{day}"
        case 4:
            month = data["month"]
            day = data["day"]
            hour = convert_to_chinese_time(data["hour"])
            return f"當前選擇時間 {year}/{month}/{day} {hour}"
        case _:
            return 'error "nowSet" input'


def SaveTimeDate(data, year: str, month: str, day: str, isToday: bool, isOY: bool):
    """
    將使用者選取的時間資料傳入data字典中
    :param data: 字典
    :param year: 使用者選取年份
    :param month: 使用者選取月份
    :param day: 使用者選取日期
    :param isToday: 使否為今天
    :param isOY:
    :return:
    """
    data.update({
        "year": year,
        "month": month,
        "day": day,
        "is_today": isToday,
        "isOY": isOY
    })


def message_check_text(data):
    """
    檢查訊息是否過長，並給出相對應所需之訊息
    :param data: 使用者輸入資料
    :return:
    """
    if len(data['text']) <= 1900:
        edit_message = f"是否選擇{data['year']}/{str(data['month']).zfill(2)}/{str(data['day']).zfill(2)} \
            \n{convert_to_chinese_time(data['hour'])}{minute_to_chinese(data['minute'])}提醒\n提醒事項：{data['text']}"
    else:
        edit_message = f"是否選擇{data['year']}/{str(data['month']).zfill(2)}/{str(data['day']).zfill(2)} \
            \n{convert_to_chinese_time(data['hour'])}{minute_to_chinese(data['minute'])}提醒\n提醒上述事項"
    return edit_message


def minute_to_chinese(minute):
    """
    分鐘轉換
    :param minute: 分鐘數
    :return:
    """
    if minute == 0:
        return "整"
    if 0 < minute < 10:
        return f"0{minute}分"
    else:
        return f"{minute}分"


def hour_check_button(data):
    """
    檢查時間並輸出按鈕選項
    :param data:
    :return:
    """
    if data["is_today"]:
        if data["hour"] == time_hour():
            set_minute_button = InlineKeyboardMarkup(minute_select(True))
            return set_minute_button
        else:
            set_minute_button = InlineKeyboardMarkup(minute_select(False))
            return set_minute_button
    else:
        set_minute_button = InlineKeyboardMarkup(minute_select(False))
        return set_minute_button


def hour_check_need(data):
    """
    檢查分鐘並給出相應小時
    :param data:
    :return:
    """
    if data["is_today"]:
        if time_minute() > 57:
            set_select_hour = time_hour() + 1
            return set_select_hour
        else:
            set_select_hour = time_hour()
            return set_select_hour
    else:
        set_select_hour = 0
        return set_select_hour


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Telegram error:", exc_info=context.error)
    await bot.sendMessage(DEV_ID, f"TG機器人發生了神奇的錯誤：{context.error}")


# stop = True


# not use
# def check():
#     """
#     後臺查詢功能
#     :return:
#     """
#     global stop
#     try:
#         while stop:
#             # 使用者輸入查詢資料
#             need_get = input("請輸入需要讀取的資料\n")
#             id_match = re.search(r'(\d+)id', need_get)
#             lot_id_match = re.search(r'(\d+)lid', need_get)
#             if need_get == "user":
#                 print("user_data", json.dumps(user_data, indent=2, ensure_ascii=False))
#             elif need_get == "data":
#                 print(f"[{time_datetime()}] 當前尚未通知的有: ")
#                 for item in GetNotUseData():
#                     formatted_item = f"ID:{item[0]:<4} {item[2]} {item[1]}"
#                     print(formatted_item)
#             elif need_get == "file":
#                 CheckFile()
#             elif need_get == "clear":
#                 print("\033c")
#             elif id_match:
#                 get_Need_Id = str(id_match.group(1))
#                 print(f"[{time_datetime()}] {get_Need_Id}資料: \n")
#                 for item in GetIdData(get_Need_Id):
#                     if item:
#                         formatted_item = f"ID:{item[0]:<4} |提醒時間: {item[2]} |提醒事項: \n{item[1]}"
#                         print(formatted_item)
#                     else:
#                         print('na')
#             elif need_get == "all":
#                 print(f"[{time_datetime()}] 所有資料: \n")
#                 for item in GetAllData():
#                     item1 = str(item[1]).replace("\n", " ")
#                     formatted_item = f"ID:{item[0]:<4} |提醒時間: {item[2]} |提醒事項: {item1[:50]}"
#                     print(formatted_item)
#             elif lot_id_match:
#                 Lot_id = int(lot_id_match.group(1))
#                 if Lot_id == 1:
#                     FirstId = 1
#                     LestId = 50
#                 else:
#                     FirstId = ((Lot_id - 1) * 50) + 1
#                     LestId = Lot_id * 50
#                 for item in GetLotId(FirstId, LestId):
#                     item1 = str(item[1]).replace("\n", " ")
#                     formatted_item = f"ID:{item[0]:<4} |提醒時間: {item[2]} |提醒事項: {item1[:50]}"
#                     print(formatted_item)
#             else:
#                 print("無法讀取\n可輸入：user以及data")
#     except KeyboardInterrupt:
#         stop = False
#     except EOFError:
#         stop = False
#         print(f"[{time_datetime()}] 檢測到使用者按下ctrl+c，正在關閉機器人...")
#     else:
#         sys.exit()


def app():
    """
    開啟機器人
    :return:
    """
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_error_handler(error_handler)
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("機器人已上線")
    logger.info('機器人已上線')
    application.run_polling()


def CheckFile():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schedule';")
    result = cursor.fetchone()
    # 检查结果
    if not result:
        logger.warning("数据库中不存在名为 'schedule' 的表，正在創建 'schedule' 表")
        cursor.execute('''
        CREATE TABLE "schedule"
        (
        ID       INTEGER
            primary key,
        Message  TEXT    default 'No Message' not null,
        UserID   INTEGER default -1           not null,
        ChatID   INTEGER default -1           not null,
        DateTime TEXT    default -1           not null,
        UserTime TEXT    default 'na',
        Send     TEXT    default 'False'
        );
                        ''')
        logger.warning("'schedule' 表創建完成")
    conn.commit()
    conn.close()


def main():
    """
    程式入口
    :return:
    """
    # global stop
    # UserThread = threading.Thread(target=check, daemon=True)
    try:
        # UserThread.start()
        CheckFile()
        app()
    except:
        logger.error('有東西抱錯了: ', exc_info=True)
        return
    finally:
        logger.info('logger end')


if __name__ == "__main__":
    main()
