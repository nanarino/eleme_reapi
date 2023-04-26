import eleme_reapi as ele
import db, pathlib
from colorama_terminal import Colormsg, proportion_bar
from eleme_reapi.tools.circuit_breaker import circuit_breaker, CircuitFused
import time
import argparse
parser = argparse.ArgumentParser(description='任务分发')
parser.add_argument('shop_list', nargs='+')
args = parser.parse_args()
shop_list = args.shop_list
SKUOUT_ERROR_set = set()
es = ele.sender(source="39893", secret='******')
cb = circuit_breaker(5)
#shop_list = ["32267603631"]

with db.conn.log() as log, db.conn.org() as org:

    for shop_id in shop_list:
        
        with open(pathlib.Path('./4_get_sku_list.sql')) as sql:
            sku_list = org.execute(sql, {"shop_id": shop_id}).fetchall()

        c = 0
        l = len(sku_list)

        for custom_sku_id, category_id in sku_list:

            while 1:
                try:
                    body = {
                        "shop_id": shop_id,
                        "custom_sku_id": custom_sku_id,
                        "category_id": category_id
                    }
                    res = es.request(cmd="sku.shop.category.map", body=body)
                    if errno := res['body']['errno']:
                        log.execute(f"""INSERT INTO "main"."catMap"
                                ("time", "goodscode", "errno", "error")
                            VALUES 
                                ({repr(time.time())}, {repr(custom_sku_id)}, {errno}, {repr(res['body']['error'].replace("'",'').replace('"',''))})
                        """)
                        log.commit()
                        print(
                            Colormsg(
                                f"{shop_id}-{custom_sku_id} 接口返回不合预期 :{res['body']['error']}"
                            ).set_color('MAGENTA'))

                        if errno == 50001: # 功能4绑定失败的或功能2创建失败的
                            SKUOUT_ERROR_set.add(custom_sku_id)
                            cb.shift(True)
                            break
                        time.sleep(1)
                        cb.shift(False)
                        continue
                    cb.shift(True)
                    break
                except Exception as e:
                    print(Colormsg(f"{shop_id}-{e}").set_color('MAGENTA'))
                    try:
                        time.sleep(1)
                        cb.shift(False)
                    except CircuitFused:
                        print(Colormsg("熔断器触发，后续任务无法进行").set_color('RED'))
                        proportion_bar(c / l, 'RED')
                        input("已停止工作，按任意键退出")
                        exit()
                    continue
            c += 1
            proportion_bar(c / l, 'CYAN')
            print(f'\t{shop_id}\t{custom_sku_id}')

if SKUOUT_ERROR_set:
    print('本次遇到的功能4未绑定或绑定失败导致的错误的goodscode列表为：')
    print(repr(tuple(SKUOUT_ERROR_set)))
    
input("已停止工作，按任意键退出")
