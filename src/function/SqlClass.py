import os
import mysql.connector
from dotenv import load_dotenv

from src.function.loggr import logger

load_dotenv()


class Sql:
    def __init__(self):
        self._DB = os.getenv('DB')
        self._host = os.getenv('HOST')
        self._DatabaseUser = os.getenv('DatabaseUser')
        self._password = os.getenv('PASSWORD')
        self._conn = None
        self._cursor = None

    def connect(self):
        try:
            self._conn = mysql.connector.connect(
                host=self._host,
                database=self._DB,
                user=self._DatabaseUser,
                password=self._password
            )
            self._cursor = self._conn.cursor()
            if self._conn.is_connected() and self._cursor is not None:
                logger.info('已連接至資料庫')
        except mysql.connector.errors.DatabaseError:
            logger.error(f'嘗試連接資料庫錯誤 ', exc_info=True)
        except mysql.connector.errors.InterfaceError:
            logger.error(f'使用者帳號密碼錯誤 ', exc_info=True)

    def sendConnect(self):
        try:
            self._conn = mysql.connector.connect(
                host=self._host,
                database=self._DB,
                user=self._DatabaseUser,
                password=self._password
            )
            self._cursor = self._conn.cursor()
        except mysql.connector.errors.DatabaseError:
            logger.error(f'嘗試連接資料庫錯誤 ', exc_info=True)
        except mysql.connector.errors.InterfaceError:
            logger.error(f'使用者帳號密碼錯誤 ', exc_info=True)

    def Close(self):
        try:
            self._cursor.close()
            self._conn.close()
            if self._conn is None:
                logger.info('已關閉資料庫連接')
        except mysql.connector.Error:
            logger.error(f'嘗試關閉資料庫連接錯誤 ', exc_info=True)

    def QueryData(self, sql, data=None):
        try:
            tupleData = data
            if isinstance(data, list):
                logger.info('data is array, turn to tuple')
                tupleData = tuple(data)
            return self._query(sql, tupleData)
        except mysql.connector.errors.IntegrityError:
            logger.error(f'抓取數據時發生錯誤: 數據完整性違規 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.DataError:
            logger.error(f'抓取數據時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'抓取數據時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'抓取數據時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)

    def insertData(self, tableName, columns, data):
        sql = None
        try:
            tupleData = tuple(data)
            columnsString = str(columns).replace("'", "`")
            sql = f"""
            INSERT INTO {tableName} {columnsString} VALUES ({', '.join(['%s'] * len(columns))})
            """
            self._cursor.execute(sql, tupleData)
            self._conn.commit()
        except mysql.connector.errors.DataError:
            logger.error(f'插入數據時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'插入數據時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'插入數據時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)

    def DoSqlData(self, sql, data):
        try:
            self._cursor.execute(sql, data)
            self._conn.commit()
        except mysql.connector.errors.DataError:
            logger.error(f'執行sql其他資料修改時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'執行sql其他資料修改時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'執行sql其他資料修改時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)

    def DoSql(self, sql):
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except mysql.connector.errors.OperationalError:
            logger.error(f'執行sql語句時發生錯誤: 數據庫操作失敗 {sql}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'執行sql語句時發生錯誤: sql語法錯誤 {sql}', exc_info=True)

    def _query(self, query, data):
        if data is None:
            self._cursor.execute(query)
            results = self._cursor.fetchall()
            return results
        self._cursor.execute(query, data)
        results = self._cursor.fetchall()
        return results
