from pony.orm import *

from lib.lbTool.ConfigManager import ConfigManager


def get_orm_con():
    """
    获取数据库连接
    :return:
    """
    db_config = ConfigManager.get_value("database")
    if db_config['driver'] == "oracle":
        db_con = Database("oracle", user=f"{db_config['user']}", password=f"{db_config['password']}",
                          dsn=f"{db_config['host']}:{db_config['port']}/{db_config['db_name']}")
    elif db_config['driver'] == "mysql":
        db_con = Database("mysql", host=f"{db_config['host']}", port=db_config['port'], user=f"{db_config['user']}",
                          password=f"{db_config['password']}",
                          db=f"{db_config['db_name']}")
    else:
        raise RuntimeError("不支持的数据库连接！")
    return db_con


def init_con(db_con, is_create_table=False, show_sql=True):
    """
    初始化db
    :param db_con: db对象
    :param is_create_table: 是否创建表
    :param show_sql: 是否在控制台显示语句
    :return:
    """
    if show_sql:
        # 控制台显示语句
        sql_debug(True)
    create_table = True if is_create_table is True else False
    # 根据实体关联表
    db_con.generate_mapping(create_tables=create_table)


class Db:
    def __init__(self, db_con, is_create_table=False, show_sql=True):
        """
        获取数据库操作对象
        :param db_con: 数据库连接对象
        :param is_create_table: 是否创建数据表
        :param show_sql: 是否在控制台显示语句
        """
        self.db = db_con
        if show_sql:
            # 控制台显示语句
            sql_debug(True)
        create_table = True if is_create_table is True else False
        # 根据实体关联表
        self.db.generate_mapping(create_tables=create_table)

    @db_session
    def query(self, entity_cls, **filters):
        """
        查询单条
        :param entity_cls: 实体类
        :param filters: 查询条件
        :return:
        """
        return entity_cls.select(**filters).first()

    @db_session
    def query_list(self, entity_cls, **filters):
        """
        查询列表
        :param entity_cls: 实体类
        :param filters: 查询条件
        :return:
        """
        return entity_cls.select(**filters).fetch()[:]

    @db_session
    def query_page_list(self, entity_cls, page_num=1, page_size=10, **filters):
        """
        查询列表
        :param entity_cls: 实体类
        :param page_num: 页码
        :param page_size: 每页数量
        :param filters: 查询条件
        :return:
        """
        return entity_cls.select(**filters).page(page_num, page_size)[:]

    @db_session
    def query_count(self, entity_cls, **filters):
        """
        查询总数
        :param entity_cls: 实体类
        :param filters: 查询条件
        :return:
        """
        return entity_cls.select(**filters).count()

    @db_session
    def insert(self, entity_cls, **kwargs):
        """
        新增
        :param entity_cls: 实体类
        :param kwargs: 字段信息
        :return:
        """
        return entity_cls(**kwargs)

    @db_session
    def update(self, entity, **kwargs):
        """
        修改（需要使用`with db_session`语句块）
        :param entity: 实体
        :param kwargs: 需更新的数据
        :return:
        """
        for attr, value in kwargs.items():
            setattr(entity, attr, value)

    @db_session
    def remove(self, entity):
        """
        删除
        （执行查询后调用删除需要使用`with db_session`语句块，否则会提示会话中断）
        :param entity: 实体
        :return:
        """
        entity.delete()

    @db_session
    def remove_batch(self, entity_cls, **kwargs):
        """
        批量删除
        :param entity_cls: 实体类
        :param kwargs: 删除条件
        :return:
        """
        entity_cls.select(**kwargs).delete(bulk=True)

    @db_session
    def execute(self, sql, params=None, local_params=None):
        """
        执行语句
        :param sql: 原始语句
        :param params: 全局变量
        :param local_params: 可选参数
        :return:
        """
        return self.db.execute(sql, params, local_params)
