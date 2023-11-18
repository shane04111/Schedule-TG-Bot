import os

from src.function.SqlClass import Sql

DBHandler = Sql()


def GetData():
    """
    抓取時間比目前還要早並且尚未通知使用者過的訊息
    :return:
    """
    results = DBHandler.QueryData('''
    SELECT Message, ChatID, ID 
    FROM schedule
    WHERE `DateTime` <= SYSDATE()
    AND Send = 'False';
    ''')
    return results


def ChangeSendTrue(delID: str):
    """
    將提檢查提醒欄位轉為已提醒
    :param delID:
    :return:
    """
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = %s;"
    data = [delID]
    DBHandler.DoSqlData(sql, data)
