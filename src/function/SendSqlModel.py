from src.function.SqlClass import Sql

DBHandler = Sql()


def GetData() -> list[tuple]:
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


def getError() -> list[tuple]:
    """
    抓取時間比目前還要早並且尚未通知使用者過的訊息
    :return:
    """
    results = DBHandler.QueryData('''
    SELECT Message, ChatID, ID 
    FROM Schedule.Error
    WHERE `DateTime` <= SYSDATE()
    AND Send = 'False';
    ''')
    return results


def change(delID: int, table: int = 1 | 2) -> None:
    """
    將提檢查提醒欄位轉為已提醒
    :param table:
    :param delID:
    :return:
    """
    if table == 1:
        sql = "UPDATE Schedule.Error SET Send = 'True' WHERE ID = %s;"
    else:
        sql = "UPDATE Schedule.schedule SET Send = 'True' WHERE ID = %s;"
    data = (delID, )
    DBHandler.DoSqlData(sql, data)
