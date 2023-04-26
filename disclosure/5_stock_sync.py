import eleme_reapi as ele
import db, time, json
from functools import reduce, partial
from colorama_terminal import Colormsg, proportion_bar
from eleme_reapi.tools.parse import list_reshape, batch
from eleme_reapi.tools.circuit_breaker import circuit_breaker, retry
es = ele.sender(source="39893", secret='******')
def stock_sync(shop_list):# 清空缓存 truncate table E_eleme_stock
    cb = circuit_breaker(5)
    with db.conn.log() as log, db.conn.org() as org:
        for shop_id in shop_list:
            c = 0
            org_data = org.execute(f'get_stock_change_by_eleme_mdbh {repr(shop_id)}').fetchall()
            slice_data = list_reshape(org_data, 100)
            l = len(slice_data)
            def request(qs):
                body = {'shop_id': shop_id, 'custom_sku_id': batch(dict(qs))}
                res = es.request(cmd="sku.stock.update.batch", body=body)
                None_goods_list = []
                if errno := res['body']['errno']:
                    error = res['body']['error']
                    if errno == 500001: # 商品不存在
                        failed_list = (json.loads(res['body']['error']))["failed_list"]
                        for failed in failed_list:
                            log.execute(f"""INSERT INTO "main"."syncFailed"
                                    ("time", "shop_id", "goodscode", "errno", "error")
                                VALUES 
                                    ({time.time()!r}, 
                                    {shop_id!r}, 
                                    {failed['custom_sku_id']!r}, 
                                    {failed['error_no']!r}, 
                                    {failed['error_msg'].replace("'",'').replace('"','')!r})
                            """)
                        log.commit()
                        None_goods_list = list(reduce(lambda x,y: x+[y['custom_sku_id']], failed_list, []))
                    else:
                        raise ele.senderror(errno, error) #接口返回不合预期
                else:
                    pass
                nonlocal c
                c += 1
                proportion_bar(c / l, 'CYAN')
                print(f'\t{shop_id}\t')
                return None_goods_list
            
            def err_callback(error_info:tuple):
                proportion_bar(c / l, 'RED')
                print(Colormsg(f"\t{shop_id}\t{error_info!r}").set_color('RED'))
                if len(error_info) != 2 : return
                log.execute(f"""INSERT INTO "main"."syncFailed"
                                    ("time", "shop_id", "goodscode", "errno", "error")
                                VALUES 
                                    ({time.time()!r}, 
                                    {shop_id!r}, 
                                    'slice_data', 
                                    {error_info[0]!r}, 
                                    {error_info[1].replace("'",'').replace('"','')!r})
                            """)
                log.commit()
                
            tasks = map(lambda qs: partial(request, qs), slice_data)
            None_goods_list = (retry(tasks, ele.senderror, err_callback, cb))
            org.commit()
            None_goods_tuple = tuple(reduce(lambda x,y: x+y, None_goods_list, []))
            if None_goods_tuple:
                print(f'以下标品在饿了么门店{shop_id}里不存在，请补充创建商品')
                print(None_goods_tuple)

if __name__ == "__main__":
    input('请按回车键开始...')
    shop_list = (
        '32267603639',
        '32267603636',
        '32267603633',
        '32267603632',
        '32267377314',
        '32267347288',
        '32267347287',
        '32267347286',
        '32267311608',
        '32267311607',
        '32267311606',
        '32267311605',
        '32267311604'
    )
    stock_sync(shop_list)
    input("已完成，按回车键退出")
