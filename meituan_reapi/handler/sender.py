from ..computed import sign
from collections import OrderedDict
import requests, json
from requests import RequestException
from ..tools import retry_for_good
from typing import Mapping, Optional


class senderror(Exception):
    '''发送失败 默认错误信息是【发送失败：网络错误】'''
    def __init__(self, err: str = '发送失败：网络错误'):
        super().__init__(err)


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

    def request(self, api: str, body: Mapping, method: Optional[str] = 'POST') -> dict:
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

        if method.upper() == 'GET':
            res_obj = retry_for_good(lambda : requests.get(self.url + self.version + api, params=req), error=RequestException)
        elif method.upper() == 'POST':
            res_obj = retry_for_good(lambda : requests.post(self.url + self.version + api, data=req), error=RequestException)
        else:
            raise TypeError("参数错误：method参数只有‘GET’和‘POST’两种选择")

        if (status_code:=res_obj.status_code) == 200:
            res = res_obj.json()
        else:
            raise senderror(f"发送失败：HTTP状态码不符合预期，{status_code=}，{req=}")

        return res
