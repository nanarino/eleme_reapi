from .ticket import ticket
from .timestamp import timestamp
from collections import OrderedDict
from ..tools import parse
import hashlib
from ..handler import sender


def sign(data: OrderedDict) -> str:
    md5 = hashlib.md5()
    md5.update(parse.url(data).encode())
    return md5.hexdigest().upper()


def remix(ele_sender: sender, cmd: str, body: str) -> OrderedDict:
    data = OrderedDict()
    data["body"] = body
    data["cmd"] = cmd
    data.update(ele_sender.public_args)
    data["ticket"] = ticket()
    data["timestamp"] = timestamp()
    data.move_to_end("version", last=True)
    data['sign'] = sign(data)
    return data