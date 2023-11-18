from src.function.SqlClass import Sql
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
        'Schedule.schedule', ('Message', 'UserID', 'ChatID', 'DateTime', 'UserTime'),
        (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00", time_datetime()))


def ChangeSendTrue(delID: str):
    """
    將提檢查提醒欄位轉為已提醒
    :param delID:
    :return:
    """
    sql = "UPDATE Schedule.schedule SET Send = 'True' WHERE ID = %s;"
    data = [delID]
    DBHandler.DoSqlData(sql, data)


def GetUserMessage(userId, chatID):
    """
    抓取特定使用這在特定頻道之提醒訊息
    :param userId: 使用者ID
    :param chatID: 使用者所在頻道ID
    :return:
    """
    sql = "SELECT ID, Message, DateTime FROM Schedule.schedule WHERE Send = 'False' AND UserID = %s AND ChatID = %s;"
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
    FROM Schedule.schedule 
    WHERE UserID = %s
    AND ChatID = %s
    ORDER BY ID 
    DESC LIMIT 5;"""
    data = [userId, chatID]
    return DBHandler.QueryData(sql, data)


def GetIdData(GetId):
    """
    抓取特定id資料
    :return:
    """
    sql = "SELECT ID, Message, DateTime FROM Schedule.schedule WHERE ID = %s;"
    data = [GetId, ]
    return DBHandler.QueryData(sql, data)


def GetIdUserData(GetId, userId, chatId):
    """
    抓取特定id資料
    :return:
    """
    sql = """
    SELECT ID, Message, DateTime 
    FROM Schedule.schedule 
    WHERE ID = %s
    AND UserID = %s
    AND ChatID = %s;
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
    FROM Schedule.schedule
    WHERE ID 
    BETWEEN %s 
    AND %s;
    """
    data = [IdFirst, IdLest, ]
    return DBHandler.QueryData(sql, data)
