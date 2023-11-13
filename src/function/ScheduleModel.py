import os

from src.function.SqlClass import Sql
from src.function.loggr import logger
from src.function.my_time import time_datetime

DBHandler = Sql()


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
    DBHandler.insertData(
        'schedule', ('Message', 'UserID', 'ChatID', 'DateTime', 'UserTime'),
        (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00", time_datetime()))


def ChangeSendTrue(delID: str):
    """
    將提檢查提醒欄位轉為已提醒
    :param delID:
    :return:
    """
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = ?;"
    data = [delID]
    DBHandler.DoSqlData(sql, data)


def GetUserMessage(userId, chatID):
    """
    抓取特定使用這在特定頻道之提醒訊息
    :param userId: 使用者ID
    :param chatID: 使用者所在頻道ID
    :return:
    """
    sql = "SELECT ID, Message, DateTime FROM schedule WHERE Send == 'False' AND UserID = ? AND ChatID = ?;"
    data = [userId, chatID]
    return DBHandler.QueryData(sql, data)


def GetUserDoneMessage(userId, chatID):
    """
    抓取特定使用這在特定頻道之已提醒訊息
    :param userId: 使用者ID
    :param chatID: 使用者所在頻道ID
    :return:
    """
    sql = """
    SELECT ID, Message, DateTime 
    FROM schedule 
    WHERE UserID = ? 
    AND ChatID = ? 
    ORDER BY ID 
    DESC LIMIT 5;"""
    data = [userId, chatID]
    return DBHandler.QueryData(sql, data)


def GetIdData(GetId):
    """
    抓取特定id資料
    :return:
    """
    sql = "SELECT ID, Message, DateTime FROM schedule WHERE ID == ?;"
    data = [GetId, ]
    return DBHandler.QueryData(sql, data)


def GetIdUserData(GetId, userId, chatId):
    """
    抓取特定id資料
    :return:
    """
    sql = """
    SELECT ID, Message, DateTime 
    FROM schedule 
    WHERE ID == ? 
    AND UserID == ? 
    AND ChatID == ?;
    """
    data = [GetId, userId, chatId, ]
    return DBHandler.QueryData(sql, data)


def GetLotId(IdFirst: int, IdLest: int):
    """
        抓取特定區間id資料
        :return:
    """
    sql = """
    SELECT ID, Message, DateTime 
    FROM schedule 
    WHERE ID 
    BETWEEN ? 
    AND ?;
    """
    data = [IdFirst, IdLest, ]
    return DBHandler.QueryData(sql, data)


def CheckFile():
    result = DBHandler.QueryData("SELECT name FROM sqlite_master WHERE type='table' AND name='schedule';")
    # 检查结果
    if not result:
        logger.warning("数据库中不存在名为 'schedule' 的表，正在創建 'schedule' 表")
        DBHandler.DoSql('''
        CREATE TABLE IF NOT EXISTS "schedule"
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
