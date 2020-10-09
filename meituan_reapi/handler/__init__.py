"""核心请求模块

包括:
    sender: 文档接口请求
    senderror: 统一的api请求错误类 方便熔断器捕获
"""

__all__ = ['sender']

from .sender import *
