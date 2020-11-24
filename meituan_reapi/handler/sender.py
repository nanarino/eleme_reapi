from ..computed import sign
from collections import OrderedDict
import requests, json
from requests import RequestException
from ..tools import retry_for_good
from typing import Mapping, Optional


class senderror(Exception):
    '''发送失败'''
    def __init__(self, *args):
        super().__init__(*args)


class sender:
    """美团接口请求类.

    Args：
        app_id: 对接方账号.
        app_secret: 私钥.
   
    Attributes: 
        url: 默认的接口域名（前缀）.
        version: 默认的版本.
    """
    url = "https://waimaiopen.meituan.com/"
    version = "api/v1/"

    def __init__(self, app_id: int, app_secret: str):
        self.data = OrderedDict([('app_id', app_id)])
        self.app_secret = app_secret

    def request(self,
                api: str,
                body: Mapping,
                method: Optional[str] = 'POST') -> dict:
        '''发送请求

        Args:
            api: 接口地址去掉域名版本等前缀，如"medicine/save".
            method: 请求方式 默认'POST'.
            body: 请求业务对应的参数。详见'https://open-shangou.meituan.com/'.
            body["app_poi_code"]: APP方门店id.
        
        Returns:
            req：请求的全部数据. 请求方式为None会返回req
            res：返回的全部数据，经过了反序列化.
        '''

        req = dict(sign.remix(self, api, body))

        if method is None:
            return req

        def try_send():
            '''发起请求 超时或状态码不是200将会无限重试（频率15秒）'''
            if method.upper() == 'GET':
                r = requests.get(self.url + self.version + api, params=req)
            elif method.upper() == 'POST':
                r = requests.post(self.url + self.version + api, data=req)
            else:
                raise TypeError("参数错误：method参数只有‘GET’和‘POST’两种选择")
            r.raise_for_status()
            return r.json()

        return retry_for_good(try_send, RequestException)
