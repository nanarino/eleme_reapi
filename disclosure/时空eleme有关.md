# 饿了么相关

添加字段：

- 门店库存脏检查：`ogbalance.eleme_dirt`
- 门店编号：`orgdoc.eleme_poicode`



### 	查询门店库存（脏）

```sql
select a.goodsid, b.ownerid, b.placenum
from goodsdoc a 
join ogbalance b on a.goodsid = b.goodsid 
where b.ownerid = 'FD000000FDG' --东方店
and b.eleme_dirt = 'Y'
and
```



### 创建脏检查触发器

```sql
CREATE TRIGGER dbo.placenum_on_update
   ON  dbo.OGBALANCE  
   AFTER UPDATE
AS 
BEGIN
	SET NOCOUNT ON;
	if update(placenum)
	begin
	UPDATE a SET eleme_dirt = 'Y' 
	FROM OGBALANCE a 
	JOIN inserted b ON a.GoodsId = b.goodsid AND a.OrgId = b.orgid AND a.OwnerId = b.ownerid AND a.EntId = b.entid
	end
END
```



