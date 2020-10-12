'''美团同步的接口调用模块

实际上是美团闪购接口，文档: https://open-shangou.meituan.com/.

主要功能:
    eleme_reapi.sender: 文档接口调用类
'''

__version__ = "0.0.3"

__all__ = ['handler', 'computed', 'tools']

from .handler import *

from . import computed

from . import tools