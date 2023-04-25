import eleme_reapi as ele
import db
from eleme_reapi.tools.parse import list_reshape
import time
shop_list = ["32267603684"]
es = ele.sender(source="39893", secret='******')
print(shop_list)
with db.conn.org() as org:
    lll = [(16033591762213494,),(1603355203226676,),]
    for shop_id in shop_list:
        data = lll
        data = list_reshape(list(map(lambda x: str(x[0]), data)), 100)
        for i in data:
            
            body = {
                "shop_id": shop_id,
                "sku_id": ','.join(i),
            }
            
            res = es.request(cmd="sku.delete", body=body)
            '''
            if errno := res['body']['errno']:
                for j in json.loads(res['body']['error'])['failed_list']:
                    print(j)
            '''
            print(1)
            time.sleep(1)
input()