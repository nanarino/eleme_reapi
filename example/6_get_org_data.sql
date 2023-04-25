select g.goodscode, 100*g.elejgtx*o.RetailP as cents
from GORELAT o
  join goodsdoc g on o.goodsid = g.goodsid
  join orgdoc org on org.orgid = o.OrgId
  join ogbalance oo on o.goodsid = oo.goodsid and o.orgid=oo.ownerid
where g.ele_tag = 'A' 
  and g.is_ele_std = 'Y'
  and org.eleme_mdbh = ?