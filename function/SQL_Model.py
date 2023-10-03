from function.my_time import *
import os
import sqlite3

from dotenv import load_dotenv

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
    conn.commit()
    conn.close()


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
        '''INSERT INTO schedule (Message, UserID, ChatID, DateTime, UserTime) VALUES (?, ?, ?, ?, ?)''',
        (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00", time_datetime()))
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
    conn.close()
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
    conn.close()
    return results


def ChangeSendTrue(delID: str):
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
    conn.close()


def ChangeSendFalse(delID: str):
    """
    將提檢查提醒欄位轉為未提醒
    :param delID:
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = ?;"
    data = [delID]
    cursor.execute(sql, data)
    conn.commit()
    conn.close()


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
    conn.close()
    return results


def GetUserDoneMessage(userId, chatID):
    """
    抓取特定使用這在特定頻道之已提醒訊息
    :param userId: 使用者ID
    :param chatID: 使用者所在頻道ID
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    sql = "SELECT ID, Message, DateTime FROM schedule WHERE Send == 'True' AND UserID = ? AND ChatID = ?;"
    data = [userId, chatID]
    cursor.execute(sql, data)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def GetAllData():
    """
    抓取所有訊息
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Message, DateTime FROM schedule;")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def GetIdData(GetId):
    """
    抓取特定id資料
    :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Message, DateTime FROM schedule WHERE ID == ?;", [GetId, ])
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results


def GetLotId(IdFirst: int, IdLest: int):
    """
        抓取特定區間id資料
        :return:
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Message, DateTime FROM schedule WHERE ID BETWEEN ? AND ?;", [IdFirst, IdLest, ])
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results
