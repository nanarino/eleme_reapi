import random


def _random_hex(n):
    """生成n位长度的随机十六进制字符串"""
    return hex(random.randint(0, 16**n))[2:].zfill(n)


def ticket():
    """生成请求饿百接口所需的ticket参数"""
    ticket_arr = [_random_hex(i) for i in (8, 4, 4, 4, 12)]
    return '-'.join(ticket_arr).upper()


if __name__ == "__main__":
    print(ticket())