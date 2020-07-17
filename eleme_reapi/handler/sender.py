from ..computed import sign
from collections import OrderedDict
import requests
import json
from ..tools.parse import Decimal_as_int_Encoder


class sender:
    """饿百接口请求类.

    Args：
        source: 对接方账号.
        secret: 私钥.
        encrypt: 加密方式，默认'des.v1'.
        fields: 返回结果中过滤以及字段，多个字段用分隔符|分割，默认'a|b'.
        version: 版本，默认3.0.
    
    Attributes:
        url: 接口地址.
        public_args: 接口所需的公共参数数据.
    """
    url = "https://api-be.ele.me/"

    def __init__(self,
                 source,
                 secret,
                 encrypt: str = 'des.v1',
                 fields: str = 'a|b',
                 version = '3'):
        kwargs = OrderedDict()
        kwargs['encrypt'] = encrypt
        kwargs['fields'] = fields
        kwargs['secret'] = str(secret)
        kwargs['source'] = str(source)
        if ver := str(version):
            if (main_ver := ver[0]).isdigit():
                kwargs["version"] = main_ver
                self.public_args = kwargs
                return
        raise ValueError("实例化时参数version格式错误") 

    def request(self, cmd: str, body: dict) -> (dict, dict):
        '''发送请求

        Args:
            cmd: 请求业务对应的命令.
            body: 请求业务对应的参数。详见'https://open-be.ele.me/dev/api/apidoc'.
                由于几乎不存在参数为浮点类型的接口，Decimal类型在序列化时会被视为int类型.
            body["shop_id"]: 请求的门店id，测试账号的门店id应该是【合作方商户id】.
        
        Returns:
            （req：请求的全部数据，res：返回的全部数据）。都经过了反序列化。
        '''

        body = json.dumps(body, cls=Decimal_as_int_Encoder, sort_keys=True, separators=(',', ':'))
        req = dict(sign.remix(self, cmd, body))
        res = requests.post(self.url, data=req).json()
        return req, res
