from function.my_time import time_year, time_month, time_day, time_hour, time_minute
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
DB = os.getenv("DB")


def CheckFile():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schedule';")
    result = cursor.fetchone()
    # 检查结果
    if result:
        print("数据库中存在名为 'schedule' 的表。")
    else:
        print("数据库中不存在名为 'schedule' 的表，正在創建 'schedule' 表")
        cursor.execute('''CREATE TABLE "schedule" (
                        "ID"	    INTEGER,
                        "Message"	TEXT    NOT NULL DEFAULT 'No Message',
                        "UserID"	INTEGER NOT NULL DEFAULT -1,
                        "ChatID"	INTEGER NOT NULL DEFAULT -1,
                        "DateTime"	TEXT    NOT NULL DEFAULT -1,
                        "Send"	    TEXT             DEFAULT 'False',
                        PRIMARY KEY("ID")
                        );
                        ''')
    conn.commit()
    cursor.close()


def SaveData(Message: str, UserID: int, ChatID: int, Year: int, Month: int, Day: int, Hour: int, Minute: int):
    """
    將資料寫入資料庫中
    :param Message:     使用者輸入
    :param UserID:      使用者輸入
    :param ChatID:      使用者輸入
    :param Year:        使用者輸入
    :param Month:       使用者輸入
    :param Day:         使用者輸入
    :param Hour:        使用者輸入
    :param Minute:      使用者輸入
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO schedule (Message, UserID, ChatID, DateTime) VALUES (?, ?, ?, ?)''',
        (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00"))
    conn.commit()
    cursor.close()


def GetData():
    """
    抓取時間比目前還要早並且尚未通知使用者過的訊息
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT Message, ChatID, ID 
    FROM schedule 
    WHERE datetime(DateTime) <= datetime('now', 'localtime') 
    AND Send == 'False';
    ''')

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    return results


def GetNotUseData():
    """
    抓取尚未提醒過的所有訊息
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Message, DateTime FROM schedule WHERE Send == 'False';")

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    return results


def ChangeSend(delID: str):
    """
    將提檢查提醒欄位轉為已提醒
    :param delID:
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = ?;"
    data = [delID]
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()


def GetUserMessage(userId, chatID):
    """
    抓取特定使用這在特定頻道之提醒訊息
    :param userId: 使用者ID
    :param chatID: 使用者所在頻道ID
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    sql = "SELECT ID, Message, DateTime FROM schedule WHERE Send == 'False' AND UserID = ? AND ChatID = ?;"
    data = [userId, chatID]
    cursor.execute(sql, data)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    return results
