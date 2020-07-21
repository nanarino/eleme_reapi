"""数据签名处理模块"""
from .ticket import ticket
from .timestamp import timestamp
from collections import OrderedDict
from ..tools import parse
import hashlib
from ..handler import sender


def sign(data: OrderedDict) -> str:
    """对数据计算签名值计算"""
    md5 = hashlib.md5()
    md5.update(parse.url(data).encode())
    return md5.hexdigest().upper()


def remix(ele_sender: sender, cmd: str, body: str) -> OrderedDict:
    """计算签名并混入数据使最终满足接口请求格式

    Args:
        ele_sender: 实例化的饿百接口请求类，带有初始化的接口所需的公共参数数据.
        cmd: 请求业务对应的命令.
        body: 请求业务对应的参数JSON。详见https://open-be.ele.me/dev/api/apidoc.

    Returns:
        有序字典，最终满足接口请求格式的数据.该函数不会对sender对象的属性进行修改.
    """
    data = OrderedDict()
    data["body"] = body
    data["cmd"] = cmd
    data.update(ele_sender.public_args)
    data["ticket"] = ticket()
    data["timestamp"] = timestamp()
    data.move_to_end("version", last=True)
    data['sign'] = sign(data)
    return data