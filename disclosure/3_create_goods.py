import eleme_reapi as ele
import db, traceback, pathlib
from colorama_terminal import Colormsg, proportion_bar
from eleme_reapi.tools.circuit_breaker import circuit_breaker, CircuitFused
from re import match
import time
import argparse
parser = argparse.ArgumentParser(description='任务分发')
parser.add_argument('shop_list', nargs='+')
args = parser.parse_args()
shop_list = args.shop_list
es = ele.sender(source="39893", secret='******')
cb = circuit_breaker(7)
ig_set = set()

with db.conn.log() as log, db.conn.org() as org:
    for shop_id in shop_list:
        c = 0
        with open(pathlib.Path('./3_create_goods.py')) as sql:
            goods_list = org.execute(sql, (shop_id,)).fetchall()

        l = 2 * len(goods_list)
        # 创建商品
        for upc, goodscode, name, left_num, price in goods_list:
            while 1:
                try:
                    body = {
                        'shop_id': shop_id,
                        'upc': upc,
                        'name': name.strip(),
                        'status': 1,
                        'left_num': int(left_num),
                        'sale_price': int(price)
                    }
                    res = es.request(cmd="sku.create", body=body)
                    if errno := res['body']['errno']:
                        error = res['body']['error']
                        print(
                            Colormsg(
                                f"{shop_id}-{goodscode} 接口返回不合预期 :{error}"
                            ).set_color('MAGENTA'))
                        log.execute(f"""INSERT INTO "main"."skuMap"
                                ("time", "goodscode", "errno", "error")
                            VALUES 
                                ({repr(time.time())}, {repr(goodscode)}, {errno}, {repr(error.replace("'",'').replace('"',''))})
                        """)
                        log.commit()
                        if errno == 500001: # 商品已存在
                            sku_id = error.split('sku_id')[1][1:]
                            cb.shift(True)
                            break
                        elif errno == 5004: #该药品存在异常，请删除条码对应的连锁产品、门店商品后重新创建
                            sku_id = 'error'
                            cb.shift(True)
                            break
                        elif errno == 1: #SPU已禁用，不允许创建
                            sku_id = 'error'
                            cb.shift(True)
                            break
                        elif errno == 1000:
                            #{errorCodes:[{errorParam:
                            #{MSG:{\\IC_CATEGORY_CPV_FREEZE\\:\\该属性值【拜耳】在类目上已被冻结，禁止使用;
                            #具体禁用的是【维生素类】类目下，【品牌】中的【拜耳】，请尝试修改后再操作；
                            #若无法修改请您先对该型号产品纠错，待纠错审批通过后再重新操作。
                            #(类目Id:[201233405] ,属性Id: [20000], 属性值Id: [43365])\\}},
                            #key:systemError,mesCode:THD_IC_PUBLISH_MERCHANT_PRODUCT_ERROR,
                            #message:IC发布商家产品失败,错误信息:
                            #{\\IC_CATEGORY_CPV_FREEZE\\:\\该属性值【拜耳】在类目上已被冻结，禁止使用;
                            #具体禁用的是【维生素类】类目下，【品牌】中的【拜耳】，请尝试修改后再操作；
                            #若无法修改请您先对该型号产品纠错，待纠错审批通过后再重新操作。
                            #(类目Id:[201233405] ,属性Id: [20000], 属性值Id: [43365])\\},type:error}],
                            #extra:{},firstErrorCode:{$ref:$.errorCodes[0]},ignore:false,success:false}
                            sku_id = 'error'
                            cb.shift(True)
                            break
                        elif errno == 2: # RPC调用异常

                            # 常见错误1
                            # RPC调用异常-[systemError:IC_IC_SAVE_INVENTORY_TO_IP_FAILED:
                            # 保存库存失败: [调用库存中心失败，可能是HSF超时，
                            # productId:616275336470].:]null

                            # 常见错误2
                            # RPC调用异常-[systemError:IC_IC_CHECKSTEP_SPU_NOT_EXIST:
                            # 根据行业规定，本类目下新发商品必须匹配标准产品。
                            # 当前你的商品没有匹配到标准产品，
                            # 请点此链接https://baike.taobao.com/create.htm?catId=[201219730]\xa0 
                            # 申请一个标准产品。:]null

                            # 常见错误3
                            # RPC调用异常-[systemError:IC_IC_CATEGORY_CPV_FREEZE:
                            # 该属性值【拜耳】在类目上已被冻结，禁止使用;
                            # 具体禁用的是【维生素类】类目下，【品牌】中的【拜耳】，请尝试修改后再操作；
                            # 若无法修改请您先对该型号产品纠错，待纠错审批通过后再重新操作。
                            # (类目Id:[201233405] ,属性Id: [20000], 属性值Id: [43365]):]null

                            if match('aIC_IC_SAVE_INVENTORY_TO_IP_FAILED', error) is None:
                                sku_id = 'error'
                                # org.execute(f"""update goodsdoc set ele_tag = '' where {goodscode=}""")
                                # org.commit()
                                cb.shift(True)
                                break
                        time.sleep(1)
                        cb.shift(False)
                        continue
                    try:
                        sku_id = res['body']['data']['sku_id']
                    except TypeError:
                        sku_id = 'error'
                    cb.shift(True)
                    break
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
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
            print(f'\t{shop_id}\t{goodscode}')
            # 映射自定义ID
            while 1:

                try:

                    if sku_id == 'error':
                        ig_set.add(goodscode)
                        sku_id = '已知错误忽略'
                        cb.shift(True)
                        break

                    body = {
                        "shop_id": shop_id,
                        "sku_id": int(sku_id),
                        "custom_sku_id": goodscode
                    }
                    res = es.request(cmd="sku.shop.customsku.map",
                                     body=body)
                    if res['body']['errno']:
                        print(res)
                        print(
                            Colormsg(
                                f"{shop_id}-{sku_id} 接口返回不合预期 :{res['body']['error']}"
                            ).set_color('MAGENTA'))
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
            print(f'\t{shop_id}\t{sku_id}')

if ig_set:
    print('本次忽略的错误的goodscode列表为：')
    print(repr(tuple(ig_set)))
    print('请根据日志决定是否去除它的ele_tag')
input("已停止工作，按任意键退出")
