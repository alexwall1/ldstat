create view professional_area_per_county as
select
	count(p.id) as num_posts,
	sum(p.num_jobs) as num_jobs,
	c.id as county_id,
	c.name as county_name,
	pa.id as professional_area_id,
	pa.name as professional_area_name,
	bp.batch_id as batch_id
from
	post as p inner join
	municipality as m on p.municipality_id = m.id inner join
	county as c on m.county_id = c.id inner join
	profession as pr on p.profession_id = pr.id inner join
	professional_group as pg on pr.professional_group_id = pg.id inner join
	professional_area as pa on pg.professional_area_id = pa.id inner join
	batch_post as bp on bp.post_id = p.id
group by
	c.id,
	c.name,
	pa.id,
	pa.name,
	bp.batch_id