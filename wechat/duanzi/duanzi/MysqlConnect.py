import pymysql

"""
    本模块是对mysql数据库代码的封装，实现了增删改查的功能
"""


class MysqlHelper(object):
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="password", mysqldb="house", charset="utf8"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.mysqldb = mysqldb
        self.charset = charset

    # 连接数据库
    def get_connection(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                        db=self.mysqldb, charset=self.charset)
        except Exception as e:
            print("数据库连接失败：", e)
            return False
        self.cur = self.conn.cursor()
        return True

    # 执行数据库插入数据
    def insert(self, sql, params=None):
        if not self.get_connection():
            print("ERROR：数据库连接错误")
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("insert:", sql, "::ERROR")
            print(e)
            return False
        return True

    # 删除数据库中数据
    def delete(self, sql, params=None):
        if not self.get_connection():
            print("ERROR：数据库连接错误")
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("delete:", sql, "::ERROR")
            print(e)
            return False
        return True

    # 更新数据库数据
    def update(self, sql, params=None):
        if not self.get_connection():
            print("ERROR：数据库连接错误")
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print("update:", sql, "::ERROR")
            print(e)
            return False
        return True

    # 根据id来查询一条数据
    def find_one_by_id(self, sql, params=None):
        if not self.get_connection():
            print("ERROR：数据库连接错误")
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                result = self.cur.fetchone()
        except Exception as e:
            print("find_one_by_id:", sql, "::ERROR")
            print(e)
            return False
        return result

    # 查询所有符合条件的数据
    def find_all(self, sql, params=None):
        if not self.get_connection():
            print("ERROR：数据库连接错误")
            return False
        try:
            if self.conn and self.cur:
                self.cur.execute(sql, params)
                result = self.cur.fetchall()
        except Exception as e:
            print("find_all:", sql, "::ERROR")
            print(e)
            return False
        return result

    # 数据量统计操作
    def count(self, sql, params):
        if not self.get_connection():
            return False
        try:
            if self.conn and self.cur:
                count = self.cur.execute(sql, params)
        except Exception as e:
            print("count:", sql, "::ERROR")
            print(e)
            return False
        return count

    # 关闭数据库连接
    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
