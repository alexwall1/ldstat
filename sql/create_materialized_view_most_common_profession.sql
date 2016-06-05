create materialized view most_common_profession as
select
	match_data->>'yrkesbenamning' as profession,
	sum(case when published >= '2016-02-01' and published <= '2016-02-29' then 1 else 0 end) as c2,
	rank() over(order by sum(case when published >= '2016-02-01' and published <= '2016-02-29' then 1 else 0 end) desc) as rank2,
	sum(case when published >= '2016-03-01' and published <= '2016-03-31' then 1 else 0 end) as c3,
	rank() over(order by sum(case when published >= '2016-03-01' and published <= '2016-03-31' then 1 else 0 end) desc) as rank3,
	sum(case when published >= '2016-04-01' and published <= '2016-04-30' then 1 else 0 end) as c4,
	rank() over(order by sum(case when published >= '2016-04-01' and published <= '2016-04-30' then 1 else 0 end) desc) as rank4
from
	post as p
where
	published >= '2016-02-01' and published <= '2016-04-30'
group by
	profession
order by
	c4 desc
limit 100;