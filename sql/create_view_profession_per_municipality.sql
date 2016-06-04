create view profession_per_municipality as
select
	count(p.id) as num_posts,
	sum(p.num_jobs) as num_jobs,
	c.id as county_id,
	c.name as county_name,
        m.id as municipality_id,
        m.name as municipality_name,
	pr.id as profession_id,
        pr.name as profession_name,
        pa.id as professional_area_id,
	pa.name as professional_area_name,
        pg.id as professional_group_id,
        pg.name as professional_group_name,
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
        m.id,
        m.name,
        pr.id,
        pr.name,
	pa.id,
	pa.name,
        pg.id,
        pg.name,
	bp.batch_id
