from src.function.ScheduleModel import DBHandler
from src.function.loggr import logger
from src.function.my_time import time_datetime


def start(user: int, chat: int, message: int, userMessage: int, text: str = None):
    columns = ('UserID', 'ChatID', 'MessageID', 'UserMessageID', 'Text', 'StartTime')
    data = (user, chat, message, userMessage, text, time_datetime(),)
    DBHandler.insertData('Schedule.UserData', columns, data)


class UserDataInsert:
    def __init__(self, ID):
        self._databaseID = ID
        self._data = []
        self._setSql = []

    def Text(self, text):
        self._setSql.append(f"Text = %s")
        self._data.append(text)
        return self

    def Year(self, year):
        self._setSql.append(f"Year = %s")
        self._data.append(year)
        return self

    def Month(self, Month):
        self._setSql.append(f"Month = %s")
        self._data.append(Month)
        return self

    def Day(self, Day):
        self._setSql.append(f"Day = %s")
        self._data.append(Day)
        return self

    def Hour(self, Hour):
        self._setSql.append(f"Hour = %s")
        self._data.append(Hour)
        return self

    def Minute(self, Miner):
        self._setSql.append(f"Miner = %s")
        self._data.append(Miner)
        return self

    def CheckDone(self, CheckDone):
        self._setSql.append(f"CheckDone = %s")
        self._data.append(CheckDone)
        return self

    def isToday(self, isToday):
        self._setSql.append(f"isToday = %s")
        self._data.append(isToday)
        return self

    def isOY(self, isOY):
        self._setSql.append(f"isOY = %s")
        self._data.append(isOY)
        return self

    def done(self):
        self._setSql.append("CheckDone = 'True'")
        self._setSql.append(f"EndTime = %s")
        self._data.append(time_datetime())
        return self

    def _setData(self):
        if len(self._setSql) == 1:
            return self._setSql[0]
        return ' , '.join(self._setSql)

    def _setDB(self):
        self._data.append(self._databaseID)
        return tuple(self._data)

    def insert(self):
        # todo 修改成插入
        sql = f"""
        UPDATE Schedule.UserData
        SET {self._setData()} 
        WHERE ID = %s;
        """
        data = self._setDB()
        logger.debug(self._setData())
        logger.debug(data)
        DBHandler.DoSqlData(sql, data)


class UserData:
    def __init__(self,
                 UserID: int = None,
                 ChatID: int = None,
                 MessageID: int = None,
                 UserMessageID: int = None,
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
        self.userMessageID = UserMessageID


def CheckUser(user, chat, message):
    sql = """
    SELECT 
    UserID, 
    ChatID, 
    MessageID, 
    Text, 
    Year, 
    Month, 
    Day, 
    Hour, 
    Miner, 
    CheckDone, 
    isToday, 
    isOY, 
    ID, 
    UserMessageID
    FROM Schedule.UserData
    WHERE UserID = %s
    AND ChatID = %s
    AND MessageID = %s
    """
    data = (user, chat, message)
    result = DBHandler.QueryData(sql, data)
    if len(result) != 1:
        logger.error(f'預期只有一筆資料，但回傳了 {len(result)} 筆資料\ndata: {result}\nFile: "{__file__}", line 150')
        return UserData(User=False)
    if not result:
        return UserData(User=False)
    is_user = True
    user_id = int(result[0][0])
    chat_id = int(result[0][1])
    message_id = int(result[0][2])
    text = str(result[0][3])
    year = int(result[0][4])
    month = int(result[0][5])
    day = int(result[0][6])
    hour = int(result[0][7])
    minute = int(result[0][8])
    check = eval(result[0][9])
    is_today = eval(result[0][10])
    is_oy = eval(result[0][11])
    database_id = int(result[0][12])
    user_message_id = int(result[0][13])
    return UserData(user_id, chat_id, message_id, user_message_id, text, year, month, day, hour, minute, check,
                    is_today, is_oy, is_user, database_id)
