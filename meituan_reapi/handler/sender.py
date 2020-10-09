from ..computed import sign
from collections import OrderedDict
import requests, json
from requests import RequestException
from ..tools.circuit_breaker import retry_five_times


class senderror(Exception):
    '''发送失败'''
    def __init__(self, err='发送失败：发送失败，网络错误'):
        Exception.__init__(self, err)

def raise_senderror():
    '''抛出发送失败的异常'''
    raise senderror


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

    def __init__(self, app_id, app_secret):
        self.data = OrderedDict([('app_id',app_id)])
        self.app_secret = app_secret

    def request(self, api: str, body: dict, method: str = 'POST') -> dict:
        '''发送请求

        Args:
            api: 接口地址去掉域名版本等前缀，如"medicine/save"
            method: 请求方式 默认'POST'，如果为None会返回req（请求的全部数据）
            body: 请求业务对应的参数。详见'https://open-shangou.meituan.com/'.
            body["app_poi_code"]: APP方门店id.
        
        Returns:
            res：返回的全部数据，经过了反序列化。
        '''

        req = dict(sign.remix(self, api, body))

        if method is None:
            return req

        if method.upper() == 'GET':
            res_obj = retry_five_times(
                lambda : requests.get(self.url + self.version + api, params=req),
                error=RequestException,
                circuit_fused_callback=raise_senderror)
        elif method.upper() == 'POST':
            res_obj = retry_five_times(
                lambda : requests.post(self.url + self.version + api, data=req),
                error=RequestException,
                circuit_fused_callback=raise_senderror)
        else:
            raise ValueError("参数错误：method参数只有‘GET’和‘POST’两种选择")

        if (status_code:=res_obj.status_code) == 200:
            res = res_obj.json()
        else:
            raise senderror(f"发送失败：响应状态不符合预期，{status_code=}，{req=}")

        return res
