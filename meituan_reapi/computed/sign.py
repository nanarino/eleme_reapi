"""数据签名处理模块"""
from .timestamp import timestamp
from collections import OrderedDict
from ..tools import parse
import hashlib
from ..handler import sender


def sign(data: OrderedDict, all_api_url: str, app_secret: str) -> str:
    """对数据计算签名值计算"""
    md5 = hashlib.md5()
    md5.update((all_api_url + '?' + parse.url(data) + app_secret).encode())
    return md5.hexdigest()


def remix(mt_sender: sender, api: str, body: str) -> OrderedDict:
    """计算签名并混入数据使最终满足接口请求格式

    Args:
        mt_sender: 实例化的美团接口请求类，带有初始化的接口所需的公共参数数据.
        api: 请求业务对应的api.
        body: 请求业务对应的参数.

    Returns:
        有序字典，最终满足接口请求格式的数据.该函数不会对sender对象的属性进行修改.
    """
    data = mt_sender.data
    data.update(body)
    data['timestamp'] = timestamp()
    data = OrderedDict(sorted(data.items(), key=lambda x: x[0]))
    all_api_url = mt_sender.url + mt_sender.version + api
    data['sig'] = sign(data, all_api_url, mt_sender.app_secret)
    return data