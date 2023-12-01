from src.function.SqlClass import Sql
from src.function.loggr import logger
from src.function.my_time import time_datetime

DBHandler = Sql()


class SqlModel:
    def __init__(self):
        self.db = DBHandler

    def SaveData(self,
                 Message: str, UserID: int,
                 ChatID: int, Year: int,
                 Month: int, Day: int,
                 Hour: int, Minute: int) -> None:
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
        self.db.insertData(
            'Schedule.schedule', ('Message', 'UserID', 'ChatID', 'DateTime', 'UserTime'),
            (Message, UserID, ChatID, f"{Year}-{Month}-{Day} {Hour}:{Minute}:00", time_datetime()))

    def saveError(self,
                  Message: str, UserID: int,
                  ChatID: int) -> None:
        """
        將資料寫入資料庫中
        :param Message:     使用者輸入
        :param UserID:      使用者輸入
        :param ChatID:      使用者輸入
        :return:
        """
        self.db.insertData(
            'Schedule.Error', ('Message', 'UserID', 'ChatID'),
            (Message, UserID, ChatID))

    def showNumber(self, userId: int, chatId: int) -> list[tuple[int]]:
        sql = """
        SELECT COUNT(*) as record_count
        FROM Schedule.schedule
        WHERE UserID = %s 
        AND ChatID = %s;
        """
        data = (userId, chatId,)
        return self.db.QueryData(sql, data)

    def showAllNumber(self) -> list[tuple[int]]:
        sql = """
        SELECT COUNT(*) as record_count
        FROM Schedule.schedule;
        """
        return self.db.QueryData(sql)

    def ChangeSendTrue(self, delID: str) -> None:
        """
        將提檢查提醒欄位轉為已提醒
        :param delID:
        :return:
        """
        sql = "UPDATE Schedule.schedule SET Send = 'True' WHERE ID = %s;"
        data = (delID,)
        self.db.DoSqlData(sql, data)

    def GetUserMessage(self, userId: int, chatID: int) -> list[tuple]:
        """
        抓取特定使用這在特定頻道之提醒訊息
        :param userId: 使用者ID
        :param chatID: 使用者所在頻道ID
        :return:
        """
        sql = """
        SELECT ID, Message, DateTime 
        FROM Schedule.schedule 
        WHERE Send = 'False' 
        AND UserID = %s 
        AND ChatID = %s
        ORDER BY ID DESC;
        """
        data = (userId, chatID,)
        return self.db.QueryData(sql, data)

    def GetUserDoneMessage(self,
                           userId: int,
                           chatID: int,
                           number: int = 5,
                           sort: str = 'DESC') -> list[tuple]:
        """
        抓取特定使用這在特定頻道之已提醒訊息
        :param userId: 使用者ID
        :param chatID: 使用者所在頻道ID
        :param number:
        :param sort:
        :return:
        """
        sql = """
        SELECT ID, Message, DateTime 
        FROM Schedule.schedule 
        WHERE UserID = %s
        AND ChatID = %s
        ORDER BY ID 
        {sort} LIMIT %s;"""
        data = (userId, chatID, number,)
        return self.db.QueryData(sql, data)

    def GetIdData(self, GetId: int) -> list[tuple] | None:
        """
        抓取特定id資料
        :return:
        """
        sql = "SELECT ID, Message, DateTime FROM Schedule.schedule WHERE ID = %s;"
        data = (GetId,)
        final = self.db.QueryData(sql, data)
        if len(final) != 1:
            logger.error(f'預期只有一筆資料，但回傳了 {len(final)} 筆資料\ndate: {final}\nFile "{__file__}",line 121')
            return None
        return final

    def GetIdUserData(self, get_id: int, user: int, chat: int) -> list[tuple]:
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
        data = (get_id, user, chat,)
        return self.db.QueryData(sql, data)

    def showData(self, user: int, chat: int, number: int) -> list[tuple]:
        sql = """
        SELECT ID, Message, DateTime 
        FROM Schedule.schedule 
        WHERE UserID = %s
        AND ChatID = %s
        ORDER BY ID
        LIMIT 10 OFFSET %s;
        """
        data = (user, chat, number,)
        return self.db.QueryData(sql, data)

    def showAllData(self, number: int) -> list[tuple]:
        sql = """
        SELECT ID, Message, DateTime 
        FROM Schedule.schedule 
        ORDER BY ID
        LIMIT 10 OFFSET %s;
        """
        data = (number,)
        return self.db.QueryData(sql, data)

    def getMessageID(self, chat: int, message: int) -> list[tuple]:
        sql = """
        SELECT MessageID, ID
        FROM Schedule.UserData
        WHERE ChatID = %s
        AND UserMessageID = %s
        """
        data = (chat, message,)
        return self.db.QueryData(sql, data)

    def getCopy(self, chat: int, message: int) -> list[tuple]:
        sql = """
        SELECT UserMessageID, ID
        FROM Schedule.UserData
        WHERE ChatID = %s
        AND MessageID = %s
        """
        data = (chat, message,)
        return self.db.QueryData(sql, data)

    def editText(self, number: int, text: str) -> None:
        sql = """
        UPDATE Schedule.UserData
        SET `Text` = %s
        WHERE ID = %s;
        """
        data = (text, number,)
        self.db.DoSqlData(sql, data)
