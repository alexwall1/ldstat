create materialized view most_common_profession as
select
	match_data->>'yrkesbenamning' as profession,
	sum(case when published >= '2016-02-01' and published <= '2016-02-29' then 1 else 0 end) as c2,
	sum(case when published >= '2016-03-01' and published <= '2016-03-31' then 1 else 0 end) as c3,
	sum(case when published >= '2016-04-01' and published <= '2016-04-30' then 1 else 0 end) as c4
from
	post as p
	--- batch_post as bp inner join
	--- post as p on bp.post_id = p.id inner join
	--- batch as b on bp.batch_id = b.id
where
	published >= '2016-02-01' and published <= '2016-04-30'
group by
	profession
order by
	c4 desc
limit 100;