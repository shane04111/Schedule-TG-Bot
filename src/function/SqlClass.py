import os
import sqlite3
from src.function.loggr import logger

_FILE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_FILEPATH = f"{_FILE}/data/schedule_data.db"


class Sql:
    def __init__(self):
        self.DB = _FILEPATH
        self._conn = None
        self._cursor = None

    def connect(self):
        try:
            self._conn = sqlite3.connect(self.DB)
            self._cursor = self._conn.cursor()
            logger.info('已連接至資料庫')
        except sqlite3.Error:
            logger.error('try to connect database error ', exc_info=True)

    def sendConnect(self):
        try:
            self._conn = sqlite3.connect(self.DB)
            self._cursor = self._conn.cursor()
        except sqlite3.Error:
            logger.error('try to connect database error ', exc_info=True)

    def Close(self):
        try:
            self._conn.close()
            logger.info('已關閉資料庫連接')
        except sqlite3.Error:
            logger.error('try to close database error ', exc_info=True)

    def QueryData(self, query, data=None):
        try:
            if data is not None:
                self._cursor.execute(query, data)
                results = self._cursor.fetchall()
                return results
            else:
                self._cursor.execute(query)
                results = self._cursor.fetchall()
                return results
        except sqlite3.Error:
            logger.error('try query database error ', exc_info=True)

    def insertData(self, tableName, columns, data):
        sql = f"""
        INSERT INTO {tableName} {columns} VALUES ({', '.join(['?'] * len(columns))})
        """
        self._cursor.execute(sql, data)
        self._conn.commit()

    def DoSqlData(self, sql, data):
        try:
            self._cursor.execute(sql, data)
            self._conn.commit()
        except sqlite3.Error:
            logger.error('try insert data error ', exc_info=True)

    def DoSql(self, sql):
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except sqlite3.Error:
            logger.error('try to do the sql statement error ', exc_info=True)
