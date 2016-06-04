create materialized view distinct_num_posts_per_county_professional_area_week as
select
	p.professional_area_id as professional_area_id,
	pa.name as professional_area_name,
	c.id as county_id,
	c.name as county_name,
	count(distinct(bp.post_id)) as distinct_num_posts,
	date(b.start_time) as start_time
from
	post as p inner join
	batch_post as bp on p.id = bp.post_id inner join
	professional_area as pa on p.professional_area_id = pa.id inner join
	county as c on p.county_id = c.id inner join
	batch as b on bp.batch_id = b.id
group by
	professional_area_id,
	professional_area_name,
	c.id,
	county_name,
	start_time
order by
    start_time;