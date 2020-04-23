"""序列化功能"""
from collections import OrderedDict
from functools import reduce


def url(data: OrderedDict) -> str:
    """将字典序列化为url格式但是不编码"""
    if not data: return
    url_after_qm = ''
    for k, v in data.items():
        url_after_qm += f'&{k}={v}'
    return url_after_qm[1:]


def list_reshape(li: list, size: int) -> list:
    """将一维列表转化为每个成员最大长度为size的二维列表"""
    def set_size(a, v):
        a[-1].append(v[1]) if v[0] % size else a.append([v[1]])
        return a

    return list(reduce(set_size, enumerate(li), []))
