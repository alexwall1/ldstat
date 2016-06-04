create materialized view distinct_num_posts_per_week_and_county as
select
	p.county_id as county_id,
	c.name as county_name,
	count(distinct(bp.post_id)) as distinct_num_posts,
	date(b.start_time) as start_time
from
	post as p inner join
	batch_post as bp on p.id = bp.post_id inner join
	county as c on p.county_id = c.id inner join
	batch as b on bp.batch_id = b.id
group by
	county_id,
	county_name,
	start_time
order by
    county_name,
    start_time;