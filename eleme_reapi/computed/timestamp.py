"""当前时间戳生成"""
import time


def timestamp():
    """生成请求饿百接口所需的timestamp参数"""
    return str(int(time.time()))


if __name__ == "__main__":
    print(timestamp())