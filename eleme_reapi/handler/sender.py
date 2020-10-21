from ..computed import sign
from collections import OrderedDict
import requests, json
from requests import RequestException
from ..tools import retry_for_good
from typing import Mapping, Optional, Union
from ..tools.parse import Decimal_as_int_Encoder


class senderror(Exception):
    '''发送失败 默认错误信息是【发送失败：网络错误】'''
    def __init__(self, err: str = '发送失败：网络错误'):
        super().__init__(err)


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
                 source: Union[str, int],
                 secret: Union[str, int],
                 encrypt: str = 'des.v1',
                 fields: str = 'a|b',
                 version: Union[str, float]= '3.0'):
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
        raise TypeError("实例化时参数version格式错误") 

    def request(self, cmd: str, body: Mapping, method: Optional[str] = 'POST') -> dict:
        '''发送请求

        Args:
            cmd: 请求业务对应的命令.
            body: 请求业务对应的参数。详见'https://open-be.ele.me/dev/api/apidoc'.
                由于几乎不存在参数为浮点类型的接口，Decimal类型在序列化时会被视为int类型.
                body["shop_id"]: 请求的门店id，测试账号的门店id应该是【合作方商户id】.
            method: 请求方式 默认'POST'.根据文档来看 目前还没有post之外的请求方式.

        Returns:
            req：请求的全部数据, 请求方式为None会返回req.
            res：返回的全部数据, 经过了反序列化.
        '''

        body = json.dumps(body, cls=Decimal_as_int_Encoder, sort_keys=True, separators=(',', ':'))
        req = dict(sign.remix(self, cmd, body))

        if method is None:
            return req
        
        if method.upper() == 'GET':
            res_obj = retry_for_good(lambda : requests.get(self.url, params=req), error=RequestException)
        elif method.upper() == 'POST':
            res_obj = retry_for_good(lambda : requests.post(self.url, data=req), error=RequestException)
        else:
            raise TypeError("参数错误：method参数只有‘GET’和‘POST’两种选择")

        if (status_code:=res_obj.status_code) == 200:
            res = res_obj.json()
        else:
            raise senderror(f"发送失败：HTTP状态码不符合预期，{status_code=}，{req=}")

        return res