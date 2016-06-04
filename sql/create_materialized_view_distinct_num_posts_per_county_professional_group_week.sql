create materialized view distinct_num_posts_per_county_professional_group_week as
select
	p.professional_group_id as professional_group_id,
	pg.name as professional_group_name,
	p.professional_area_id as professional_area_id,
	p.county_id as county_id,
	c.name as county_name,
	date(b.start_time) as start_time,
	count(distinct(bp.post_id)) as distinct_num_posts
from
	post as p inner join
	batch_post as bp on p.id = bp.post_id inner join
	professional_group as pg on p.professional_group_id = pg.id inner join
	batch as b on bp.batch_id = b.id inner join
	county as c on p.county_id = c.id
group by
	professional_group_id,
	professional_group_name,
	p.professional_area_id,
	start_time,
	county_id,
	county_name
order by
	start_time;