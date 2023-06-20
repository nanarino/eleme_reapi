--存储过程
ALTER Proc [dbo].[k_meituan_by_info]
  	@OwnerId varchar(64) --货主ID   
	,@InfoType varchar(30) --任务类型
	,@LastUpdateTime char(19) --系统时间
As

SELECT a.GoodsId,b.ApprovalNo,a.GoodsSpec,a.BarCode --,c.lshj
	,a.mtlbcode AS hzflbh,a.mtlbname AS hzflchina,a.mtjgtx,
	isnull(a.mtejlbcode,'') as mtejlbcode,isnull(a.mtejlbname,'') as mtejlbname
	INTO #spid1
	FROM GOODSDOC a(nolock)
	JOIN GOODSATTR b(nolock) on a.GoodsId=b.goodsid and a.EntId=b.EntId
	--JOIN k_t_mtlbdzb c(nolock) ON a.GoodsId=c.spid
	where a.EntId='E2CEEM27O7T' and a.BarCode <> '' 
	and	isnull(a.mtlbcode,'')<>'' and isnull(a.mtlbname,'')<>''
	and isnull(a.code_jzt,'')='A' --是否美团商品

		
	SELECT * 
	INTO #spid 
	FROM #spid1 a
	WHERE NOT EXISTS (SELECT 1 
	 	FROM (
			SELECT barcode,COUNT(*) AS js FROM #spid1
			GROUP BY barcode
			HAVING COUNT(*)>1) b WHERE b.BarCode=a.BarCode )
	

	if @InfoType='medicine_batchupdate'--药品类--批量更新药品
	begin
  
		SELECT distinct app_medicine_code  into #temp
		FROM k_meituan_medicinelog (NOLOCK)
			WHERE --EXPDATE>=REPLACE(CONVERT(CHAR(10),DATEADD(dd,-1,GETDATE()),120),'-','')+'000000'
			--AND 
			( REMARK LIKE '%标品库中没有此药品%'  or remark like '%不存在%' ) --and 1=2
		  
	SELECT * 
	into #t2 
	FROM (
		SELECT a.app_medicine_code,a.app_poi_code
			  ,CASE WHEN ISNULL(a.sku_price,'')='' THEN  0 ELSE convert(numeric(16,2),a.sku_price) END sku_price
			  ,CASE WHEN ISNULL(a.sku_stock,'')='' THEN 0 ELSE convert(numeric(16,2),a.sku_stock) END sku_stock
			  ,ROW_NUMBER()over(partition by a.app_medicine_code,a.app_poi_code order by expdate  desc) rowId
			  ,a.TaskId,a.TaskStatus
		FROM k_meituan_medicinelog a(NOLOCK)
		WHERE (a.TaskId='medicine_batchupdate' or a.TaskId='medicine_sp_ins')
		-- a.EXPORDERID='SPH00006026' AND a.app_poi_code='3526829'
	) aa 
	WHERE aa.rowId=1

	declare @app_poi_code varchar(10)
	set @app_poi_code = (select top 1  b.meituan_mdbh 
						 from ORGDOC b 
						 left join k_meituan_medicinelog a on a.app_poi_code=b.meituan_mdbh
						 where ISNULL(b.meituan_mdbh,'')<>'' and ISNULL(b.BEACTIVE,'N')='Y' 
						 group by b.meituan_mdbh
						 order by isnull(count(a.app_poi_code),0)
						 )
-- print @app_poi_code 

		--declare @h int
		--declare @stacklen int
		--set @h = convert(int, left(convert(varchar(100), getdate(), 108), 2))
		--if(@h < 18 and @h > 8) begin set @stacklen = 2000 end else set @stacklen = 100000
		
		SELECT top 100000 --(select @stacklen)
		b.GoodsId as app_medicine_code
		,d.meituan_mdbh as app_poi_code
		,a.mtejlbcode as category_code
		,a.mtejlbname as category_name
		,'1' as sequence
		,a.hzflbh as first_category_code
		,a.hzflchina as first_category_name
		,'1' as first_sequence
		,a.mtejlbcode as second_category_code
		,a.mtejlbname as second_category_name
		,'1' as second_sequence	
		,CASE WHEN b.StorNum-isnull(x.xsshl,0)>0 THEN '0' ELSE '1' end as is_sold_out
		,a.ApprovalNo as medicine_no
		,(aa.RetailP*a.mtjgtx) as price
		,a.GoodsSpec as spec
		,CEILING(b.StorNum-isnull(x.xsshl,0)) as stock
		,a.BarCode as upc
		FROM #spid a
		JOIN STORBALANCE b(nolock) ON a.GoodsId=b.GoodsId and b.EntId='E2CEEM27O7T'
		JOIN STOREHOUSE c(nolock) ON b.WHId=c.WHId AND c.WHName NOT LIKE '%不合格%' and c.EntId='E2CEEM27O7T'
		JOIN ORGDOC d(nolock) ON b.OwnerId=d.ORGID AND ISNULL(d.meituan_mdbh,'')<>''  and d.EntId='E2CEEM27O7T'
		       and ISNULL(d.BEACTIVE,'N')='Y' and d.meituan_mdbh <> '' and d.meituan_mdbh is not null
			   --and ISNULL(d.meituan_mdbh,'') =  @app_poi_code
			   --and ISNULL(d.meituan_mdbh,'') in ('5658510','6507369')
		join GORELAT aa on a.GoodsId=aa.GoodsId and d.ORGID=aa.OrgId and b.EntId=aa.EntId  
		--LEFT JOIN #t2 e ON b.GoodsId = e.app_medicine_code AND d.meituan_mdbh=e.app_poi_code
		LEFT JOIN (select SUM(basenum) as xsshl,GoodsId,OwnerId from GOODSOCCU 
				   group by GoodsId,OwnerId) x on b.GoodsId=x.GoodsId and b.OwnerId=x.OwnerId
		where  a.GoodsId NOT IN ( SELECT app_medicine_code FROM #temp)
		--and a.GoodsId in ('SPHA0002208','SPH00002831','SPH00015463','SPHA0004339','SPH00014824','SPHA0001881','SPHA0006015','SPHA0001728','SPHA0013104','SPH00014557')
		--and d.ORGID in ('FD000000FDI','FD000000FDJ','FD000000FGS')
		and d.ORGID in ('FD000000FEE','FD000000FDL','FD000000FDO','FD000000FDQ','FD000000FEX','FD000000FDV','FD000000FEO','FD000000FEL','FD000000FDA','O2U0C3ZU3JX','O2XVXNHTBKX','FD000000FEH','FD000000FDI','FD000000FDJ','FD000000FGS')
		--and d.ORGID = 'FD000000FEH'--街区店
		--and a.GoodsId in ('SPH00008958','SPH00000309')
		and CEILING(b.StorNum-isnull(x.xsshl,0)) >= 0
		--and (aa.RetailP<>ISNULL(convert(numeric(16,2),e.sku_price),0.00) 
		--OR CEILING(b.StorNum-isnull(x.xsshl,0))<>ISNULL(convert(numeric(16,2),e.sku_stock),0.00))
		order by d.meituan_mdbh desc 

		drop table #temp,#t2,#spid,#spid1
end