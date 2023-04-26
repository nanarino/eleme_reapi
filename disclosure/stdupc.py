import eleme_reapi as ele
import db
from colorama_terminal import Colormsg, proportion_bar
from eleme_reapi.tools.circuit_breaker import circuit_breaker, CircuitFused
import time
es = ele.sender(source="39893", secret='******')
cb = circuit_breaker(7)
shop_list = ["32267603684"]
new = []
import csv
filename = './饿了么标品.csv'
csvFile = open(filename, "w", encoding='utf-8', newline='')
writer = csv.writer(csvFile)
with db.conn.log() as log, db.conn.org() as org:

    for shop_id in shop_list:

        c = 0

        goods_list = org.execute(f"""
            SELECT DISTINCT barcode from goodsdoc where isnull(barcode,'')<>'' ORDER BY BarCode
        """).fetchall()
        
        
        l = len(goods_list)

        
        for (upc,) in goods_list:

            while 1:

                try:

                    body = {
                        'shop_id': shop_id,
                        'upc': upc
                    }

                    res = es.request(cmd="sku.stdupc.exist", body=body)

                    if errno := res['body']['errno']:

                        error = res['body']['error']

                        print(
                            Colormsg(
                                f"{shop_id}-{upc} 接口返回不合预期 :{error}"
                            ).set_color('MAGENTA'))

                        cb.shift(False)
                        continue

                    cb.shift(True)
                    if res['body']['data']["std_flag"]:
                        new.append(upc)
                        writer.writerow((upc,))
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
            print(f'\t{shop_id}\t{upc}')

input(new)
csvFile.close()
