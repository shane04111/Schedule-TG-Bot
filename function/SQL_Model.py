from function.my_time import time_year, time_month, time_day, time_hour, time_minute
import sqlite3
import os


def CheckFile():
    conn = sqlite3.connect('data/schedule_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schedule';")
    result = cursor.fetchone()

    # 检查结果
    if result:
        print("数据库中存在名为 'schedule' 的表。")
    else:
        print("数据库中不存在名为 'schedule' 的表，正在創建 'schedule' 表")
        cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (
                                       Message TEXT,
                                       ChatID INTEGER,
                                       Year INTEGER,
                                       Month INTEGER,
                                       Day INTEGER,
                                       Hour INTEGER,
                                       Minute INTEGER
                                    )''')
    conn.commit()
    cursor.close()
    conn.close()


def SaveData(Message: str, ChatID: int, Year: int, Month: int, Day: int, Hour: int, Minute: int):
    conn = sqlite3.connect('data/schedule_data.db')
    cursor = conn.cursor()

    cursor.execute(
        '''INSERT INTO schedule (Message, ChatID, Year, Month, Day, Hour, Minute) VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (Message, ChatID, Year, Month, Day, Hour, Minute))
    conn.commit()
    cursor.close()
    conn.close()


def GetData():
    conn = sqlite3.connect('data/schedule_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Message, ChatID FROM schedule WHERE Year = ? AND Month = ? AND Day = ? AND Hour = ? AND Minute = ?;''',
                   (time_year(), time_month(), time_day(), time_hour(), time_minute()))

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results


def GetNotUseData():
    conn = sqlite3.connect('data/schedule_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM schedule WHERE Year > ? AND Month > ? AND Day > ? AND Hour > ? AND Minute > ?;''',
                   (time_year(), time_month(), time_day(), time_hour(), time_minute()))

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results
