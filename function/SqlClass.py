import sqlite3
from function.loggr import logger


class Sql:
    def __init__(self, DB):
        self.DB = DB
        self.conn = sqlite3.connect(self.DB)
        self.cursor = self.conn.cursor()
        if self.conn:
            logger.info('資料庫已連接')

    def Close(self):
        try:
            self.conn.close()
            logger.info('已關閉資料庫連接')
        except sqlite3.Error:
            logger.error('try to close database error ', exc_info=True)

    def QueryData(self, query, data=None):
        try:
            if data is not None:
                self.cursor.execute(query, data)
                results = self.cursor.fetchall()
                return results
            else:
                self.cursor.execute(query)
                results = self.cursor.fetchall()
                return results
        except sqlite3.Error:
            logger.error('try query database error ', exc_info=True)

    def InsertData(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.conn.commit()
        except sqlite3.Error:
            logger.error('try insert data error ', exc_info=True)

    def DoSql(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except sqlite3.Error:
            logger.error('try to do the sql statement error ', exc_info=True)
