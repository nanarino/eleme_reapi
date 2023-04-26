from abc import ABCMeta  #, abstractmethod
# from typing import LiteralString
from typing import Union, Optional

class _cur_vc(metaclass=ABCMeta):
    """游标虚拟类

        内部方法不要求实现
    """
    def __init__(self, *args, **kwargs):
        pass

    def __next__(self):
        pass

    def execute(self, sql: str, replace: Optional[Union[dict, tuple]] = None):
        """执行SQL语句"""
        raise NotImplementedError

    def executemany(self, sql: str, args: list):
        """执行多条嵌入了模板的SQL语句"""
        all_sql = ''
        for i in args:
            all_sql += (sql % i + ';')
        return self.execute(all_sql)

    def fetchone(self):
        """返回执行SQL语句的结果的第一条（下一条）数据"""
        return next(self)

    def fetchall(self):
        """返回执行SQL语句的结果的全部（剩余）数据"""
        return list(self)

    def callproc(self, proc_name: str, args: tuple):
        """执行存储过程"""
        raise NotImplementedError


class _conn_vc(metaclass=ABCMeta):
    """连接虚拟类

        内部方法不要求实现
    """
    def close(self):
        """关闭连接

            未实现
        """
        raise NotImplementedError

    def commit(self):
        """提交修改

            未实现
        """
        raise NotImplementedError

    def cursor(self, *args, **kwargs):
        return _cur_vc(*args, **kwargs)


class db_vmodule(metaclass=ABCMeta):
    """数据库虚拟模块
    
        内部方法不要求实现
    """
    def connect(self, *args, **kwargs):
        """创建连接"""
        return _conn_vc(*args, **kwargs)


class Generic_db_base(metaclass=ABCMeta):
    """数据库整合基类
    
        init_args:
            db_type: 数据库模块
            info: 数据库连接信息，包含hosts，password等

        Attributes:
            db_type：数据库模块缺省值
            default_args：数据库连接信息缺省值
    """
    default_args = dict()
    db_type = db_vmodule

    def __init__(self, info: dict = dict(), db_type=None):
        if info:
            self.default_args = info
        if db_type:
            self.db_type = db_type
        conn = self.db_type.connect(**self.default_args)
        self.conn = conn
        self.cur = conn.cursor()

    def __enter__(self):
        """上下文管理 进入"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """上下文管理 退出"""
        if exc_type:
            print(exc_type)
            #print(exc_value)
            #print(traceback)

    def close(self):
        """关闭连接"""
        self.conn.close()

    def execute(self, sql: str, replace: Optional[Union[dict, tuple]] = None) -> _cur_vc:
        """执行SQL语句"""
        return self.cur.execute(sql, replace)

    def commit(self):
        """提交修改"""
        self.conn.commit()


class Return_cur_Mixin():
    """对于游标execute不返回本身的数据库类型进行同构的类"""
    def execute(self, sql: str, replace: Optional[Union[dict, tuple]] = None) -> _cur_vc:
        """执行SQL语句"""
        self.cur.execute(sql, replace)
        return self.cur
