import os

import mysql.connector
from dotenv import load_dotenv

from src.function.logger import logger

load_dotenv()


class Sql:
    def __init__(self):
        self._DB = os.getenv('DATABASE')
        self._host = os.getenv('HOST')
        self._DatabaseUser = os.getenv('DATABASE_USER')
        self._password = os.getenv('PASSWORD')

    def QueryData(self, sql: str, data: tuple | list | None = None) -> list[tuple]:
        try:
            self._connect()
            tuple_data = _dateToTuple(data)
            return self._query(sql, tuple_data)
        except mysql.connector.errors.IntegrityError:
            logger.error(f'抓取數據時發生錯誤: 數據完整性違規 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.DataError:
            logger.error(f'抓取數據時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'抓取數據時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'抓取數據時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        finally:
            self._close()

    def insertData(self, tableName: str, columns: tuple, data: tuple | list) -> None:
        sql = None
        try:
            self._connect()
            tuple_data = _dateToTuple(data)
            columns_string = str(columns).replace("'", "`")
            sql = f"""
            INSERT INTO {tableName} {columns_string} VALUES ({', '.join(['%s'] * len(columns))})
            """
            self._cursor.execute(sql, tuple_data)
            self._conn.commit()
        except mysql.connector.errors.DataError:
            logger.error(f'插入數據時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'插入數據時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'插入數據時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        finally:
            self._close()

    def DoSqlData(self, sql: str, data: tuple) -> None:
        try:
            self._connect()
            self._cursor.execute(sql, data)
            self._conn.commit()
        except mysql.connector.errors.DataError:
            logger.error(f'執行sql其他資料修改時發生錯誤: 數據錯誤，數據格式不正確 \nsql語句: {sql}\ndata: {data}',
                         exc_info=True)
        except mysql.connector.errors.OperationalError:
            logger.error(f'執行sql其他資料修改時發生錯誤: 數據庫操作失敗 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'執行sql其他資料修改時發生錯誤: sql語法錯誤 \nsql語句: {sql}\ndata: {data}', exc_info=True)
        finally:
            self._close()

    def DoSql(self, sql: str) -> None:
        try:
            self._connect()
            self._cursor.execute(sql)
            self._conn.commit()
        except mysql.connector.errors.OperationalError:
            logger.error(f'執行sql語句時發生錯誤: 數據庫操作失敗 {sql}', exc_info=True)
        except mysql.connector.errors.ProgrammingError:
            logger.error(f'執行sql語句時發生錯誤: sql語法錯誤 {sql}', exc_info=True)
        finally:
            self._close()

    def _query(self, query: str, data: tuple) -> list[tuple]:
        if data is None:
            self._cursor.execute(query)
            results = self._cursor.fetchall()
            return results
        self._cursor.execute(query, data)
        results = self._cursor.fetchall()
        return results

    def _connect(self) -> None:
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

    def _close(self) -> None:
        try:
            self._cursor.close()
            self._conn.close()
        except mysql.connector.Error:
            logger.error(f'嘗試關閉資料庫連接錯誤 ', exc_info=True)


def _dateToTuple(data: tuple | list) -> tuple:
    if isinstance(data, list):
        logger.debug('data is array, turn to tuple')
        tuple_data = tuple(data)
        return tuple_data
    return data
