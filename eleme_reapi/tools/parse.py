"""序列化等格式转换功能"""
from collections import OrderedDict
from functools import reduce
import json
import decimal


def yabee_nvarchar(data: str) -> str:
    """对数据库的不合适的中文字段进行修正"""
    if isinstance(data, str) and not data.isascii():
        try:
            s = data.encode('Latin1').decode('gb2312')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        else:
            return s
    return data


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


class Decimal_as_int_Encoder(json.JSONEncoder):
    """序列化补充类.
    
    在json.dumps时decimal类将会被视为int类
    """
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, decimal.Decimal): return int(o)
        super().default(o)


def stock_batch(batch: dict) -> str:
    """将字典转化为接口sku.stock.update.batch所需格式
    
    dict([("000",Decimal(1.0),), ("001",Decimal(2.0),)]) -> "000:1;001:2"
    """
    return json.dumps(batch, cls=Decimal_as_int_Encoder,
                      separators=(';', ':')).replace('"', '').replace(
                          '{', '').replace('}', '')
