import meituan_reapi as mt
import datetime, json, csv
from colorama_terminal import proportion_bar
date_time = int(input('格式示例:  20190212\r\n请输入日期:  ') or format(datetime.date.today(),'%Y%m%d'))
ms = mt.sender(app_id = 4418, app_secret = '******')
app_poi_code = '10269340'
day_seq_len = ms.request(api = "order/getOrderDaySeq", body = {'app_poi_code':app_poi_code}, method='GET')['data']['day_seq']

with open('order'+format(datetime.datetime.now(),'%Y%m%d%H%M%S')+'.csv', "w", encoding='utf-8-sig', newline='') as csvFile:
    writer = csv.writer(csvFile)
    header = (
        '下单时间ctime',
        '流水号day_seq',
        '订单号order_id',
        '用户填写姓名recipient_name',
        '用户填写电话recipient_phone',
        '用户填写地址recipient_address',
        '定位地区area',
        '定位城市city',
        '定位地址detail_address',
        '定位省份province',
        '定位街道town',
    )
    writer.writerow(header)
    i = 0
    for day_seq in range(1,day_seq_len+1):
        order_id = ms.request(api = "order/getOrderIdByDaySeq", body = {'app_poi_code':app_poi_code,'day_seq':day_seq,'date_time':date_time}, method='GET')['data']['order_id']
        data = ms.request(api = "order/getOrderDetail", body = {'app_poi_code':app_poi_code,'order_id':order_id}, method='GET')['data']
        data.update(data.pop('recipient_address_detail', '{}'))
        writer.writerow((
            data['ctime'],
            day_seq,
            order_id,
            data['recipient_name'],
            data['recipient_phone'],
            data['recipient_address'],
            data['area'],
            data['city'],
            data['detail_address'],
            data['province'],
            data['town'],
        ))
        proportion_bar((i:=i+1) / day_seq_len, 'MAGENTA')
input()
        
        
        

