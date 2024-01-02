import dmPython
from lib.lbTool.ConfigManager import ConfigManager


def get_dm_con():
    """
        获取数据库连接
        :return:
        """
    db_config = ConfigManager.get_value("database")
    if db_config['driver'] == "dm":
        db_con = DmDatabase(f"{db_config['host']}:{db_config['port']}", f"{db_config['user']}",
                            f"{db_config['password']}")
    else:
        raise RuntimeError("不支持的数据库连接！")
    return db_con


class DmDatabase:
    def __init__(self, dsn, user, password):
        # self.conn = None
        self.dsn = dsn
        self.user = user
        self.password = password
        try:
            self.conn = dmPython.connect(dsn=self.dsn, user=self.user, password=self.password)
            print("Dm Connection successful!")
        except dmPython.Error as ex:
            sqlstate = ex.args[0]
            print(f"达梦数据库连接失败. SQLState: {sqlstate}。错误信息：{ex}")

    # def __enter__(self):
    #     self.connect()
    #     return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    # def connect(self):
    #     try:
    #         self.conn = dmPython.connect(dsn=self.dsn, user=self.user, password=self.password)
    #         print("Connection successful!")
    #     except dmPython.Error as ex:
    #         sqlstate = ex.args[0]
    #         print(f"Connection failed. SQLState: {sqlstate}")
    #         print(f"Error message: {ex}")

    def close(self):
        try:
            self.conn.close()
            print("Connection closed.")
        except AttributeError:
            pass  # 如果连接过程中发生异常，self.conn 可能未定义

    def begin_trans(self):
        try:
            self.conn.begin()
        except dmPython.Error as ex:
            print(f"Failed to begin transaction. Error message: {ex}")

    def commit_trans(self):
        try:
            self.conn.commit()
        except dmPython.Error as ex:
            print(f"Failed to commit transaction. Error message: {ex}")

    def rollback_trans(self):
        try:
            self.conn.rollback()
        except dmPython.Error as ex:
            print(f"Failed to roll back transaction. Error message: {ex}")

    def query(self, sql, *args, **kwargs):
        try:
            cursor = self.conn.cursor()
            if args:
                cursor.execute(sql, *args)
            elif kwargs:
                cursor.execute(sql, **kwargs)
            else:
                cursor.execute(sql)
            result = cursor.fetchone()
            # 查出当前查询的列名，保存到columns
            columns = [column[0] for column in cursor.description]
            # 组合字典形式{"name":"test","age":18}
            res_data = dict(zip(columns, result))
            cursor.close()
            return res_data
        except dmPython.Error as ex:
            print(f"Query execution failed. Error message: {ex}")
            return None

    def query_list(self, sql, *args, **kwargs):
        try:
            cursor = self.conn.cursor()
            if args:
                cursor.execute(sql, *args)
            elif kwargs:
                cursor.execute(sql, **kwargs)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            # 查出当前查询的列名，保存到columns
            columns = [column[0] for column in cursor.description]
            # 定义一个数组，用来保存每一组的数组，格式为字典形式{"name":"test","age":18}
            sub_resdata = []
            for row in result:
                # 循环遍历查询出来的结果，然后生成字典
                res_data = dict(zip(columns, row))
                sub_resdata.append(res_data)
            cursor.close()
            return sub_resdata
        except dmPython.Error as ex:
            print(f"Query execution failed. Error message: {ex}")
            return None

    def execute(self, sql, *args, **kwargs):
        try:
            cursor = self.conn.cursor()
            if args:
                cursor.execute(sql, *args)
            elif kwargs:
                cursor.execute(sql, **kwargs)
            else:
                cursor.execute(sql)
            cursor.close()
        except dmPython.Error as ex:
            print(f"execute failed. Error message: {ex}")
