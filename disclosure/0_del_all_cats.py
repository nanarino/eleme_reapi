"""删除所有分类"""
import eleme_reapi as ele
import argparse
parser = argparse.ArgumentParser(description='任务分发')
parser.add_argument('shop_list', nargs='+')
args = parser.parse_args()
shop_list = args.shop_list
#shop_list = ["32267603631"]
es = ele.sender(source="39893", secret='******')

for shop_id in shop_list:

    res = es.request(cmd="sku.shop.category.get", body={"shop_id": shop_id})
    
    if errno := res['body']['errno']:

        error = res['body']['error']
    
        input(f'\t{shop_id}\t{errno}\t{error}')
        
    else:    
        for i in res['body']['data']['categorys']:
            ret = es.request(cmd="sku.shop.category.delete", body={"shop_id": shop_id, 'category_id': i['category_id']})
            print(ret['body']['error'])