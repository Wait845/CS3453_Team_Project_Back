import pymysql
import traceback
import config


IP = config.Database.IP
PORT = config.Database.PORT
USER = config.Database.USER
PASSWORD = config.Database.PASSWORD
DATABASE = config.Database.DATABASE


class DataAccess():
    def __init__(self) -> None:
        self.conn = pymysql.connect(
            host=IP,
            user=USER,
            passwd=PASSWORD,
            database=DATABASE
        )
    def execute(self, sql):
        if self.conn.open:
            self.cursor = self.conn.cursor()
        else:
            return None

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.conn.commit()
            return result
        except Exception:
            self.conn.rollback()
            print(traceback.format_exc())
            return None
        finally:
            if self.cursor:
                self.cursor.close()

    def __del__(self):
        if self.conn.open:
            self.conn.close()
