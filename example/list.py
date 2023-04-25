import eleme_reapi as ele
import pathlib
filename = pathlib.Path('---.txt')
i = 1
es = ele.sender(source="39893", secret='******')
with open(filename, "a+", encoding='utf-8', newline='') as txt:
    while i:
        body = {"shop_id": "32267603684", "page":i,'pagesize':100}
        res = es.request(cmd="sku.list", body=body)
        for k in res['body']['data']['list']:
            txt.write(repr((k['sku_id'],)) + ',')
        print(i)
        i += 1

input()