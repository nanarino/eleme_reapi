# eleme_reapi
 ~~【自用】~~ 借助Python的饿了么API **同步请求** 【eleme_reapi】模块

另外还在分支中更新了**用于美团接口**的【meituan_reapi】模块

可能只适用于医药类接口

官方API文档：https://open-be.ele.me/



## 依赖

**Python3.8.2**

```bash
requests==2.23.0
```



## 文档接口调用示例

- cmd，接口指令
- body，应用级参数

```python
import eleme_reapi as ele

es = ele.sender(source="61260", secret='185bec8dacd85500')

body = {"shop_id": "test_681501_61260", "upc": "6926603501109"}

req, res = es.request(cmd="sku.stdupc.exist", body=body)

from pprint import pprint
print('\nreq:\n')
pprint(req)
print('\nres:\n')
pprint(res)
```

输出

```python

req:

{'body': '{"shop_id":"test_681501_61260","upc":"6926603501109"}',
 'cmd': 'sku.stdupc.exist',
 'encrypt': 'des.v1',
 'fields': 'a|b',
 'secret': '185bec8dacd85500',
 'sign': 'EFE28AAF2C3D9B81875E9B53CB2D18D0',
 'source': '61260',
 'ticket': '9A39B5A2-F9D3-D91E-676B-5071DAA9E338',
 'timestamp': '1585794397',
 'version': '3'}

res:

{'body': {'data': {'std_flag': 1, 'upc': '6926603501109'},
          'errno': 0,
          'error': 'success'},
 'cmd': 'resp.sku.stdupc.exist',
 'encrypt': 'des.v1',
 'sign': 'AC2DC057B518A2350A5ABA5BD8214650',
 'source': '61260',
 'ticket': '16738AEC-53FC-4442-9FDA-119E4FBD8720',
 'timestamp': 1585794397,
 'version': '3'}
```



## 附带的爬取功能

- get_shop_category_info，爬取指定门店下的分类信息
- get_foods_by_category，爬取指定门店指定分类下的商品信息

```python
import eleme_reapi as ele

res = ele.collect.get_shop_category_info(shop_id = 2233310913)

pprint(res)
#res['result']['detail']获得分类详细列表，包括每个分类的id
```

