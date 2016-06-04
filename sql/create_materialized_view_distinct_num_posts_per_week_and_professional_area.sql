create materialized view distinct_num_posts_per_week_and_professional_area as
select
	p.professional_area_id as professional_area_id,
	pa.name as professional_area_name,
	count(distinct(bp.post_id)) as distinct_num_posts,
	date(b.start_time) as start_time
from
	post as p inner join
	batch_post as bp on p.id = bp.post_id inner join
	professional_area as pa on p.professional_area_id = pa.id inner join
	batch as b on bp.batch_id = b.id
group by
	professional_area_id,
	professional_area_name,
	start_time
order by
    professional_area_id,
    start_time;