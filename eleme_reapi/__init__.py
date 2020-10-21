'''饿了么同步的接口调用模块

实际上是饿百接口，文档: https://open-be.ele.me/dev/api/apidoc.

主要功能:
    eleme_reapi.sender: 文档接口调用类
    eleme_reapi.collect: H5接口调用函数
'''

__version__ = "0.0.4"

__all__ = ['handler', 'computed', 'tools']

from .handler import *

from . import computed

from . import tools