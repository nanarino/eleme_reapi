"""序列化功能"""
from collections import OrderedDict


def url(data: OrderedDict) -> str:
    """将字典序列化为url格式但是不编码"""
    if not data: return
    url_after_qm = ''
    for k, v in data.items():
        url_after_qm += f'&{k}={v}'
    return url_after_qm[1:]