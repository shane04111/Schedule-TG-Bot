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
        cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (
                                       Message TEXT NOT NULL,
                                       ChatID INTEGER NOT NULL,
                                       DateTime TEXT NOT NULL
                                    )''')
    conn.commit()
    cursor.close()


def SaveData(Message: str,UserID: int, ChatID: int, Year: int, Month: int, Day: int, Hour: int, Minute: int):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO schedule (Message, UserID, ChatID, DateTime) VALUES (?, ?, ?)''',
        (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00"))
    conn.commit()
    cursor.close()


def GetData():
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
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Message, DateTime FROM schedule WHERE Send == 'False';")

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    return results


def ChangeSend(delID: str):
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = ?;"
    asd = [delID]
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(sql, asd)
    conn.commit()
    cursor.close()


def GetUserMessage(userId, ):
