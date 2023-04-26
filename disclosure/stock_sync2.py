from multiprocessing import Process, JoinableQueue
import meituan_reapi as mt
ms = mt.sender(app_id = 4418, app_secret = '******')
import db, json

def p1(jq1,jq2):
    while 1:
        offset = jq1.get()
        body = {
            'app_poi_code': '10269340',
            'offset': offset,
            'limit': 200
        }
        jq1.task_done()
        try:
            res = ms.request(api = "medicine/list", body = body, method='GET')
            goodscode_set = tuple(g['app_medicine_code'] for g in res['data'] if g['app_medicine_code'])
        except Exception:
            goodscode_set = []
            jq1.put(offset)
            print(f'get    medicine/list  offset-{offset} failed & retry')
        if goodscode_set:
            jq1.put(offset + 8*200)
            jq2.put(goodscode_set)
            print(f'get    medicine/list  offset-{offset} ok')
        else:
            break
    jq1.join()
     
def p2(jq2,jq3,y):
    with db.conn.org() as org:
        while 1:
            orgdata = org.execute(f"""
                SELECT 
                g.goodscode,
                isnull(t.O2QK81G6VBX,0) as x,
                isnull(t.FD000000FDA,0) as y,
                isnull(t.O320XWTVCPZ,0) as z,
                isnull(t.FD000000FGE,0) as n,
                isnull(t.O34ZO7UDDN7,0) as m
                from (
                    select goodsid, ownerid, -1*baseNum as num from GoodsOccu where ownerid in ('O2QK81G6VBX','FD000000FDA','O320XWTVCPZ','FD000000FGE','O34ZO7UDDN7')
                    union 
                    select goodsid, ownerid, PlaceNum as num from angleBalance where ownerid in ('O2QK81G6VBX','FD000000FDA','O320XWTVCPZ','FD000000FGE','O34ZO7UDDN7')
                ) a
                pivot (
                    sum(a.num) for a.ownerid in (O2QK81G6VBX,FD000000FDA,O320XWTVCPZ,FD000000FGE,O34ZO7UDDN7)
                ) t
                join goodsdoc g on t.goodsid = g.goodsid
                where g.goodscode in {jq2.get()!r}
            """).fetchall()
            medicine_data = json.dumps(list(
            map(
                lambda x: {
                    "app_medicine_code": str(x[0]),
                    'app_poi_code': '10269340',
                    'stock': str(int(max(x[1]-y[0],0)+max(x[2]-y[1],0)+max(x[3]-y[2],0)+max(x[4]-y[3],0)+max(x[5]-y[4],0)))
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
    x = int(input('仓库 -'))
    y = int(input('大楼 -'))
    z = int(input('智能 -'))
    m = int(input('智能1 -'))
    n = int(input('智能2 -'))
    jq1 = JoinableQueue(8)
    jq2 = JoinableQueue()
    jq3 = JoinableQueue()
    for i in range(0,8*200,200): jq1.put(i)
    p1s = [Process(target=p1,args=(jq1,jq2)) for i in range(8)]
    p2s = [Process(target=p2,args=(jq2,jq3,(x,y,z,m,n,))) for i in range(8)]
    p3s = [Process(target=p3,args=(jq3,)) for i in range(15)]
    for p in p1s + p2s + p3s:
        p.daemon = True
        p.start()
    for p in p1s:
        p.join()
    input()
    input('确认完成')





