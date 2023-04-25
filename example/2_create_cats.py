import eleme_reapi as ele
import db
from colorama_terminal import Colormsg, proportion_bar
from eleme_reapi.tools.circuit_breaker import circuit_breaker, CircuitFused
import time
import argparse
import pathlib
parser = argparse.ArgumentParser(description='任务分发')
parser.add_argument('shop_list', nargs='+')
args = parser.parse_args()
shop_list = args.shop_list
es = ele.sender(source="39893", secret='******')
cb = circuit_breaker(5)
#shop_list = ["32267603631"]


def category_create(shop_id, name, rank=1, parent_category_id=0):
    '''请求sku.shop.category.create接口并返回反序列化后的res'''
    body = {
        "shop_id": shop_id,
        "parent_category_id": parent_category_id,
        "name": name,
        "rank": rank
    }
    return es.request(cmd="sku.shop.category.create", body=body)


def category_commit(org_db,
                    shop_id,
                    category_id,
                    E_catname,
                    E_catcode,
                    parent_category_id=0):
    """回写res到org数据库ele_shop_cate表"""
    with open(pathlib.Path('./2_category_commit.sql')) as sql:
        org_db.execute(sql, (shop_id, category_id, E_catname, E_catcode, parent_category_id,))
        org_db.commit()


with db.conn.org() as org:

    count_b = org.execute("select count(*) from E_catdoc").fetchone()[0]

    # 上传一级分类
    cat1_list = org.execute(
        "select distinct E_cat1name, E_cat1rank, E_cat1code from E_catdoc"
    ).fetchall()

    count_ab = len(cat1_list) + count_b

    for shop_id in shop_list:

        c = 0

        for E_cat1name, E_cat1rank, E_cat1code in cat1_list:

            while 1:

                try:

                    res = category_create(shop_id, E_cat1name, E_cat1rank)

                    if res['body']['errno']:
                        print(
                            Colormsg(
                                f"{shop_id}-{E_cat1name} 接口返回不合预期 :{res['body']['error']}"
                            ).set_color('MAGENTA'))

                        if res['body']['error'] == '店铺内分类已存在':
                            try:
                                category_id = org.execute(
                                    f"select category_id from ele_shop_cate where E_catcode = {repr(E_cat1code)}"
                                ).fetchone()[0]
                            except TypeError:
                                proportion_bar(c / count_ab, 'RED')
                                print(Colormsg(f"\t{shop_id}\t与数据库不匹配。清空该店分类重试").set_color('RED'))
                                input("已停止工作，按任意键退出")
                                exit()
                            cb.shift(True)
                            break
                        time.sleep(1)
                        cb.shift(False)
                        continue

                    else:
                        category_id = res['body']['data']['category_id']

                        category_commit(org, shop_id, category_id, E_cat1name,
                                        E_cat1code)

                    cb.shift(True)
                    break

                except Exception as e:
                    print(Colormsg(f"{shop_id}-{e}").set_color('MAGENTA'))
                    try:
                        time.sleep(1)
                        cb.shift(False)
                    except CircuitFused:
                        print(Colormsg("熔断器触发，后续任务无法进行").set_color('RED'))
                        proportion_bar(c / count_ab, 'RED')
                        input("已停止工作，按任意键退出")
                        exit()
                    continue

            c += 1
            proportion_bar(c / count_ab, 'CYAN')
            print(f'\t{shop_id}\t{E_cat1name}')

            # 上传二级分类

            cat2_list = org.execute(
                f"select E_cat2name, E_cat2rank, E_cat2code from E_catdoc where {E_cat1code=}"
            ).fetchall()

            for E_cat2name, E_cat2rank, E_cat2code in cat2_list:

                while 1:

                    try:

                        res = category_create(shop_id, E_cat2name, E_cat2rank,
                                              int(category_id))

                        if res['body']['errno']:
                            print(
                                Colormsg(
                                    f"{shop_id}-{E_cat2name} 接口返回不合预期 :{res['body']['error']}"
                                ).set_color('MAGENTA'))

                            if res['body']['error'] == '店铺内分类已存在':
                                cb.shift(True)
                                break
                            time.sleep(1)
                            cb.shift(False)
                            continue

                        category_id2 = res['body']['data']['category_id']

                        category_commit(org, shop_id, category_id2, E_cat2name,
                                        E_cat2code, category_id)

                        cb.shift(True)
                        break

                    except Exception as e:
                        print(Colormsg(f"{shop_id}-{e}").set_color('MAGENTA'))
                        try:
                            time.sleep(1)
                            cb.shift(False)
                        except CircuitFused:
                            print(Colormsg("熔断器触发，后续任务无法进行").set_color('RED'))
                            proportion_bar(c / count_ab, 'RED')
                            input("已停止工作，按任意键退出")
                            exit()
                        continue

                c += 1
                proportion_bar(c / count_ab, 'CYAN')
                print(f'\t{shop_id}\t{E_cat2name}')

input("已停止工作，按任意键退出")