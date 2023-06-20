import eleme_reapi as ele

es = ele.sender(source="39893", secret='******')

#body = {'sys_status': '4'} # 审核通过-4 新增商户-1

body = {'status': '1'} # 营业中-1 停业中-9

res = es.request(cmd="shop.list", body=body)

shop_list = list(map(lambda x:x['shop_id'], res['body']['data']))

print(shop_list)

input()
