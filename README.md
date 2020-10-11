# meituan_reapi

**从主分支eleme_reapi模块魔改而成的 不再适用于饿了么**

 ~~【自用】~~ 借助Python的美团【医药类】API **同步请求** 工具

官方API文档：https://open-shangou.meituan.com/



## 依赖

**Python3.8.2**

```bash
requests==2.23.0
```



## 文档接口调用示例

- api，接口名
- body，应用级参数

```python
import meituan_reapi as mt

ms = mt.sender(app_id=4411, app_secret='681e8b0c153321faf5e40b7fa3e7244b')

body = {
    'app_poi_code': 't_i7ISIvit9C',
    'app_medicine_code': '207010458',
    'upc': '6922049735924',
    'price': float(19.9),
    'stock': str(int(22)),
    'category_code': 'test_cat_1',
    'category_name': '测试分类1'
}

res = ms.request(api = "medicine/save", body = body)

print(res)
```





