from function.ScheduleModel import DBHandler
from function.my_time import time_datetime


def ScheduleStart(user, chat, message, text: str = None):
    columns = ('UserID', 'ChatID', 'MessageID', 'Text', 'StartTime')
    data = (user, chat, message, text, time_datetime(),)
    DBHandler.insertData('UserData', columns, data)


class DoDataInsert:
    def __init__(self):
        self._setSql = []
        self._data = []

    def Del(self):
        self._setSql.append('Delete')
        self._data.append('True')
        return self

    def Redo(self):
        self._setSql.append('Redo')
        self._data.append('True')
        return self

    def init(self, user, chat, message):
        self._setSql.append('UserID')
        self._data.append(user)
        self._setSql.append('ChatID')
        self._data.append(chat)
        self._setSql.append('MessageID')
        self._data.append(message)
        self._setSql.append('StartTime')
        self._data.append(time_datetime())
        self._doInsert()

    def _doInsert(self):
        columns = tuple(self._setSql)
        data = tuple(self._data)
        DBHandler.insertData('UserData', columns, data)


class UserDataInsert:
    def __init__(self, ID):
        self._databaseID = ID
        self._setSql = []

    def Text(self, Text):
        self._setSql.append(f"Text = '{Text}'")
        return self

    def Year(self, Year):
        self._setSql.append(f"Year = {Year}")
        return self

    def Month(self, Month):
        self._setSql.append(f"Month = {Month}")
        return self

    def Day(self, Day):
        self._setSql.append(f"Day = {Day}")
        return self

    def Hour(self, Hour):
        self._setSql.append(f"Hour = {Hour}")
        return self

    def Minute(self, Miner):
        self._setSql.append(f"Miner = {Miner}")
        return self

    def CheckDone(self, CheckDone):
        self._setSql.append(f"CheckDone = '{CheckDone}'")
        return self

    def isToday(self, isToday):
        self._setSql.append(f"isToday = '{isToday}'")
        return self

    def isOY(self, isOY):
        self._setSql.append(f"isOY = '{isOY}'")
        return self

    def done(self):
        self._setSql.append("CheckDone = 'True'")
        self._setSql.append(f"EndTime = '{time_datetime()}'")
        return self

    def _setData(self):
        if len(self._setSql) == 1:
            return self._setSql[0]
        else:
            return ' , '.join(self._setSql)

    def insert(self):
        sql = f"""
        UPDATE UserData
        SET {self._setData()} 
        WHERE ID = ?;
        """
        DBHandler.DoSqlData(sql, (self._databaseID,))


class UserData:
    def __init__(self,
                 UserID: int = None,
                 ChatID: int = None,
                 MessageID: int = None,
                 text: str = None,
                 year: int = None,
                 month: int = None,
                 day: int = None,
                 hour: int = None,
                 minute: int = None,
                 check: bool = None,
                 isToday: bool = None,
                 isOY: bool = None,
                 User: bool = None,
                 DBid: int = None
                 ):
        self.id = DBid
        self.userID = UserID
        self.chatID = ChatID
        self.messageID = MessageID
        self.text = text
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.today = isToday
        self.onlyYear = isOY
        self.checkDone = check
        self.checkUser = User


def CheckUser(user, chat, message):
    sql = """
    SELECT UserID, ChatID, MessageID, Text, Year, Month, Day, Hour, Miner, CheckDone, isToday, isOY, ID
    FROM UserData
    WHERE UserID == ?
    AND ChatID == ?
    AND MessageID == ?
    """
    data = (user, chat, message)
    result = DBHandler.QueryData(sql, data)
    if result:
        isUser = True
        UserID = int(result[0][0])
        ChatID = int(result[0][1])
        MessageID = int(result[0][2])
        Text = str(result[0][3])
        Year = int(result[0][4])
        Month = int(result[0][5])
        Day = int(result[0][6])
        Hour = int(result[0][7])
        Minute = int(result[0][8])
        Check = eval(result[0][9])
        isToday = eval(result[0][10])
        isOY = eval(result[0][11])
        databaseID = int(result[0][12])
        return UserData(UserID, ChatID, MessageID, Text,
                        Year, Month, Day, Hour, Minute,
                        Check, isToday, isOY, isUser, databaseID)
    else:
        return UserData(User=False)
