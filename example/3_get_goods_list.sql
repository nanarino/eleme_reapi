select a.barcode, a.goodscode, a.goodsname, b.placenum, 100*a.elejgtx*c.RetailP
  from goodsdoc a 
  join ogbalance b on a.goodsid = b.goodsid
  join GORELAT c on a.goodsid = c.goodsid and b.ownerid=c.orgid
  join orgdoc d on b.ownerid = d.orgid
  where 
  a.ele_tag = 'A'
  and c.retailp > 0
  and a.is_ele_std = 'Y'
  and d.eleme_mdbh = ?
  --and a.goodscode in ()