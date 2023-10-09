import sqlite3
from function.loggr import logger


class Sql:
    def __init__(self, DB):
        self.DB = DB
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.DB)
            self.cursor = self.conn.cursor()
            logger.info('已連接至資料庫')
        except sqlite3.Error:
            logger.error('try to connect database error ', exc_info=True)

    def sendConnect(self):
        try:
            self.conn = sqlite3.connect(self.DB)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            logger.error('try to connect database error ', exc_info=True)

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

    def insertData(self, tableName, columns, data):
        sql = f"""
        INSERT INTO {tableName} {columns} VALUES ({', '.join(['?'] * len(columns))})
        """
        self.cursor.execute(sql, data)
        self.conn.commit()

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
