"""核心请求模块

包括:
    collect: h5页面数据爬取
    sender: 文档接口请求
    senderror: 发送失败错误
"""

__all__ = ['sender', 'senderror', 'collect']

from .sender import sender
from .sender import senderror
from . import collect
