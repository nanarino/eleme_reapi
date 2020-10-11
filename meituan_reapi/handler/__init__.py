"""核心请求模块

包括:
    sender: 文档接口请求
    senderror: 统一的api请求异常类 方便熔断器捕获
    senderror_raiser: 套娃抛出senderror异常
"""

__all__ = ['sender']

from .sender import *