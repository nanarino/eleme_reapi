select a.goodscode,g.category_id
  from goodsdoc a 
  join ogbalance b on a.goodsid = b.goodsid
  join GORELAT c on a.goodsid = c.goodsid and b.ownerid=c.orgid
  join orgdoc d on b.ownerid = d.orgid
  join E_goods_cat e on e.goodsid = a.goodsid
  join E_catdoc f on f.E_catid = e.E_catid
  join ele_shop_cate g on f.E_cat2code = g.E_catcode
  where 
  a.ele_tag = 'A'
  and c.retailp > 0
  and a.is_ele_std = 'Y'
  and d.eleme_mdbh = :shop_id
  and g.shop_id = :shop_id
  --and a.goodscode in ()