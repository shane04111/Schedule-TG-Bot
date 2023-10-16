import os

from dotenv import load_dotenv

from function.SqlClass import Sql

load_dotenv()
_DB = os.getenv("DB")
DBHandler = Sql(_DB)


def GetData():
    """
    抓取時間比目前還要早並且尚未通知使用者過的訊息
    :return:
    """
    results = DBHandler.QueryData('''
    SELECT Message, ChatID, ID 
    FROM schedule 
    WHERE datetime(DateTime) <= datetime('now', 'localtime') 
    AND Send == 'False';
    ''')
    return results


def ChangeSendTrue(delID: str):
    """
    將提檢查提醒欄位轉為已提醒
    :param delID:
    :return:
    """
    sql = "UPDATE schedule SET Send = 'True' WHERE ID = ?;"
    data = [delID]
    DBHandler.DoSqlData(sql, data)
