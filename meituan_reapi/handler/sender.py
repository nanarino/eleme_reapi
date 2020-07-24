from ..computed import sign
from collections import OrderedDict
import requests
import json


class sender:
    """美团接口请求类.

    Args：
        app_id: 对接方账号.
        app_secret: 私钥.
   
    Attributes: 
        url: 接口域名（前缀）.
        app_secret: 私钥.
        data: 接口将要请求的数据，app_secret不在此列.
    """
    url = "https://waimaiopen.meituan.com/"
    version = "api/v1/"

    def __init__(self, app_id, app_secret):
        data = OrderedDict()
        data['app_id'] = app_id
        self.app_secret = app_secret
        self.data = data

    def request(self, api: str, body: dict) -> (dict, dict):
        '''发送请求

        Args:
            api: 接口地址去掉域名版本等前缀，如"medicine/save"
            body: 请求业务对应的参数。详见'https://open-shangou.meituan.com/'.
                Decimal类型在序列化时会被视为flaot类型.
            body["app_poi_code"]: APP方门店id.
        
        Returns:
            （req：请求的全部数据，res：返回的全部数据）。都经过了反序列化。
        '''
        req = dict(sign.remix(self, api, body))
        res = requests.post(self.url + self.version + api, data=req).json()
        return req, res
