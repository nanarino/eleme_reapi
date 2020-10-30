"""核心请求模块

包括:
    sender: 文档接口请求
    senderror: 统一的api请求异常类 方便熔断器捕获
"""

__all__ = ['sender', 'senderror']

from .sender import sender
from .sender import senderror
