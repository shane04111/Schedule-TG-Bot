from src.function.ScheduleModel import DBHandler


class UserLocal:
    def __init__(self, chat: int = None):
        self._chat = chat
        self._setSql = []
        self._data = []
        self.Language = self._getLang()
        self.Localtime = self._getLocal()
        self.OnlyAdmin = self._getOnly()
        self.Check = self._check()

    def user(self):
        self._setSql.append("chatID")
        self._data.append(self._chat)
        return self

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
        sql = f"""
        SELECT Language
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        if date:
            return date[0][0]
        else:
            return None

    def _getOnly(self):
        sql = f"""
        SELECT OnlyAdmin
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        if date:
            return date[0][0]
        else:
            return None

    def _getLocal(self):
        sql = f"""
        SELECT Localtime
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        if date:
            return date[0][0]
        else:
            return None

    def _check(self):
        sql = """
        SELECT *
        FROM Schedule.UserLocal
        WHERE chatID = %s
        """
        date = DBHandler.QueryData(sql, (self._chat,))
        if date:
            return True
        else:
            return False

    def initUserLocal(self, language: str = "en"):
        sql = ('chatID', 'Language',)
        data = (self._chat, language,)
        DBHandler.insertData('Schedule.UserLocal', sql, data)
