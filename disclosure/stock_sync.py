from multiprocessing import Process, JoinableQueue
import meituan_reapi as mt
ms = mt.sender(app_id = 4418, app_secret = '******')
import db, json

def p1(jq1,jq2):
    while 1:
        offset = jq1.get()
        jq1.task_done()
        body = {
            'app_poi_code': '10269340',
            'offset': offset,
            'limit': 200
        }
        try:
            res = ms.request(api = "medicine/list", body = body, method='GET')
            goodscode_set = tuple(g['app_medicine_code'] for g in res['data'] if g['app_medicine_code'])
        except Exception:
            jq1.put(offset)
            print(f'get    medicine/list  offset-{offset} failed & retry')
            continue
        if goodscode_set:
            jq1.put(offset + 8*200)
            jq2.put(goodscode_set)
            print(f'get    medicine/list  offset-{offset} ok')
        else:
            break
    jq1.join()
    jq1.close()
     
def p2(jq2,jq3):
    with db.conn.org() as org:
        while 1:
            orgdata = org.execute(f"""
                select g.goodscode,sum(n.num) as stock from (
                    select goodsid, ownerid, -1*baseNum as num from GoodsOccu
                    union 
                    select goodsid, ownerid, PlaceNum as num from angleBalance
                ) n
                join goodsdoc g on n.goodsid = g.goodsid
                where 
                    n.ownerid in ('O2QK81G6VBX','FD000000FDA') and 
                    g.goodscode in {jq2.get()!r}
                group by g.goodscode
            """).fetchall()
            
            medicine_data = json.dumps(list(
            map(
                lambda x: {
                    "app_medicine_code": str(x[0]),
                    'app_poi_code': '10269340',
                    'stock': str(int(x[1])-10) if int(x[1])>10 else '0'
                }, orgdata)),
                                   separators=(',', ':'))
            jq2.task_done()
            print(f'query  db/race        slice-200 ok')
            jq3.put(medicine_data)

def p3(jq3):
    while 1:
        medicine_data = jq3.get()
        body = {
            'app_poi_code': '10269340',
            'medicine_data': medicine_data
        }
        jq3.task_done()
        res = ms.request(api = "medicine/stock", body = body, method='POST')
        print(res)
    
if __name__ == '__main__':
    jq1 = JoinableQueue(8)
    jq2 = JoinableQueue()
    jq3 = JoinableQueue()
    for i in range(0,8*200,200): jq1.put(i)
    p1s = [Process(target=p1,args=(jq1,jq2)) for i in range(8)]
    p2s = [Process(target=p2,args=(jq2,jq3)) for i in range(8)]
    p3s = [Process(target=p3,args=(jq3,)) for i in range(8)]
    for p in p1s + p2s + p3s:
        p.daemon = True
        p.start()
    for p in p1s:
        p.join()
    print('获取商品完成')
    input()
    input('同步库存完成')





