import db
import meituan_reapi as mt
from meituan_reapi.tools.parse import list_reshape
import json, time

ms = mt.sender(app_id=****, app_secret='681e8b0c153321faf5e40b7fa3e7244b')

with db.conn.log() as log, db.conn.org() as org:
    orgdata = org.execute(r"""
        SELECT
        goodsid, barcode 
        from goodsdoc
        where barcode is not null and barcode <> ''
    """).fetchall()

    slice_data = list_reshape(orgdata, 200)

    for data_list in slice_data:

        medicine_data = json.dumps(list(
            map(
                lambda x: {
                    'app_medicine_code': str(x[0]),
                    'upc': str(x[1]),
                    'price': float(19.9),
                    'stock': str(int(22)),
                    'category_code': 'test_cat1',
                    'category_name': '测试分类'
                }, data_list)),
                                   separators=(',', ':'))

        req, res = ms.request(api = "medicine/batchsave", body = {
            'app_poi_code': 't_i********C',
            'medicine_data': medicine_data
        })

        if res['data'] == 'ng' and (error := res['error'])['code'] == 1:
            for d in json.loads(error['msg'].split('：')[-1]):
                log.execute(rf'''
                INSERT INTO "main"."batchsave"
                    ("time", "app_medicine_code", "error_msg")
                VALUES
                    ({repr(time.time())}, {repr(d['app_medicine_code'])}, {repr(d['error_msg'])})
                ;''')
            
            log.commit()