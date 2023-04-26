from .base import Generic_db_base, Return_cur_Mixin
import sqlite3, pymssql


class log(Generic_db_base):
    """本地日志库：sqlite3数据库
    
        参数同Generic_db_base类
    """
    default_args = {"database": "./log.db"}
    db_type = sqlite3


class org(Return_cur_Mixin, Generic_db_base):
    """主数据库：Microsoft SQL Server数据库

        参数同Generic_db_base类，info参数如下
        {
            "host": '192.168.10.1\\***',
            "user": "sa",
            "database": "demo_project",
            "password": "********"
        }
        如果缺少user和password，会以Windows账号的方式登录
    """
    default_args = {
        "host": '127.0.0.1',
        "database": "master",
    }
    db_type = pymssql
