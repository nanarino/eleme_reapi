"""生成请求参数：唯一请求标识UUID"""
import uuid


def ticket():
    """生成请求饿百接口所需的ticket参数"""
    return str(uuid.uuid1()).upper()


if __name__ == "__main__":
    print(ticket())