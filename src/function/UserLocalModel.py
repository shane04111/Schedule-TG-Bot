from src.function.ScheduleModel import DBHandler
from src.function.logger import logger


class UserLocal:
    def __init__(self, chat: int = None, user: int = None):
        self._chat = chat
        self._user = user
        self._setSql = []
        self._data = []
        self.Language = self._getLang()
        self.Localtime = self._getLocal()
        self.OnlyAdmin = self._getOnly()
        self.Style = self._get_style()
        self.Check = self._check()

    def language(self, language: str = None):
        self._setSql.append("Language")
        self._data.append(language)
        return self

    def localtime(self, localtime: str = None):
        self._setSql.append("Localtime")
        self._data.append(localtime)
        return self

    def onlyAdmin(self, admin: bool = False):
        self._setSql.append("OnlyAdmin")
        self._data.append(admin)
        return self

    def datePickStyle(self, style: int):
        self._setSql.append('datePickStyle')
        self._data.append(style)
        return self

    def update(self):
        update = ", ".join(f"{key} = %s" for key in self._setSql)
        sql = f"""
        UPDATE Schedule.UserLocal
        SET {update}
        WHERE chatID = %s
        """
        data = self._data + [self._chat]
        DBHandler.DoSqlData(sql, data)

    def _getLang(self):
        sql = """
        SELECT Language
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        return _checkData(date, 53)

    def _getOnly(self):
        sql = """
        SELECT OnlyAdmin
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        return _checkData(date, 62)

    def _getLocal(self):
        sql = """
        SELECT Localtime
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        return _checkData(date, 72)

    def _get_style(self):
        sql = """
        SELECT datePickStyle
        FROM Schedule.UserLocal
        WHERE userID = %s
        AND chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._user, self._chat,))
        return _checkData(date, 80)

    def _check(self):
        sql = """
        SELECT *
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        if date:
            return True
        return False

    def initUserLocal(self, language: str = "en"):
        sql = ('chatID', 'userID', 'Language',)
        data = (self._chat, self._user, language,)
        DBHandler.insertData('Schedule.UserLocal', sql, data)


def _checkData(date, line: int):
    if len(date) > 1:
        logger.error(f'預期只有一筆資料，但回傳了 {len(date)} 筆資料'
                     f'\ndata: {date}'
                     f'\nFile: "{__file__}", line {line}')
        return None
    if date:
        return date[0][0]
    else:
        return None
