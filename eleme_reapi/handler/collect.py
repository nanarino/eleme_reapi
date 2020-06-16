"""饿了么H5接口数据爬取模块"""
import requests
from ..tools import parse

_url = 'https://newretail.ele.me/newretail/shop/'


def get_shop_category_info(shop_id) -> dict:
    """通过饿了么h5接口爬取指定门店下的分类信息

        Args:
            shop_id: 请求的门店id，测试账号的门店id应该是【商户id】.
        
        Returns:
            res：返回的全部数据，经过了反序列化。
    """
    data = parse.url({"shop_id": shop_id})
    res = requests.get(_url + 'getshopcategoryinfo?' + data)
    if not (status_code:=res.status_code) == 200:
        return status_code
    return res.json()
    


def get_foods_by_category(shop_id, category_id) -> dict:
    """通过饿了么h5接口爬取指定门店指定分类下的商品信息

        Args:
            shop_id: 请求的门店id，测试账号的门店id应该是【商户id】.
            category_id: 分类编号，可从get_shop_category_info()返回的
                res['result']['detail']获得分类详细列表，包括每个分类的id
        
        Returns:
            res：返回的全部数据，经过了反序列化。
    """
    data = parse.url({
        "category_id": category_id,
        "shop_id": shop_id,
        "type": 1
    })
    res = requests.get(_url + 'getfoodsbycategory?' + data)
    if not (status_code:=res.status_code) == 200:
        return status_code
    return res.json()