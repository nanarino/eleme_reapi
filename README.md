# eleme_reapi
 ~~【自用】~~ 借助Python的饿百API同步请求工具



## 依赖

**Python3.8.2**

```bash
requests==2.23.0
```



## 示例

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
