from ..computed import sign
from collections import OrderedDict
import requests
import json


class sender:

    url = "https://api-be.ele.me/"

    def __init__(self,
                 source: str,
                 secret: str,
                 encrypt: str = 'des.v1',
                 fields: str = 'a|b',
                 version: str = '3'):
        kwargs = OrderedDict()
        kwargs['encrypt'] = encrypt
        kwargs['fields'] = fields
        kwargs['secret'] = secret
        kwargs['source'] = source
        kwargs["version"] = version
        self.public_args = kwargs

    def request(self, cmd: str, body: dict) -> (str, str):
        body = json.dumps(body, sort_keys=True, separators=(',', ':'))
        req = dict(sign.remix(self, cmd, body))
        res = requests.post(self.url, data=req).json()
        return req, res

