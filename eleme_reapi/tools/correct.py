"""格式校对功能"""
import warnings


def _is_yabee(data: str) -> bool:
    """对文本是否是拉丁文乱码进行校验
    
    Returns: bool
    """
    if not data.isascii():
        try:
            s = data.encode('Latin1').decode('gb2312')
        except UnicodeDecodeError:
            pass
        else:
            return s
    return False


def uni(body: dict):
    """对参数值的字符进行校验"""
    
    if yabee_list := list(filter(None, (_is_yabee(i) for i in body.values()))):
        warnings.warn(f'存在被以拉丁文解码的{yabee_list}，可能来自数据库不合适的字段类型', UnicodeWarning)


def arg(body: dict, cmd: str):
    """对参数键值的完整性进行校验"""
    pass