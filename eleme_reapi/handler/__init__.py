"""核心请求模块

包括:
    collect: h5页面数据爬取
    sender: 文档接口请求
"""

__all__ = ['sender', 'collect']

from .sender import *
from . import collect
