create materialized view profession_cp_municipality as
select
	pr.id as profession_id,
	pr.name as profession_name,
	pg.id as professional_group_id,
	pg.name as professional_group_name,
	pa.id as professional_area_id,
	pa.name as professional_area_name,
	m.id as municipality_id,
	m.name as municipality_name,
	c.id as county_id,
	c.name as county_name
from
	profession as pr inner join
	professional_group as pg on pr.professional_group_id = pg.id inner join
	professional_area as pa on pg.professional_area_id = pa.id,
	municipality as m inner join
	county as c on m.county_id = c.id;

create unique index profession_id_municipality_id on profession_cp_municipality (profession_id, municipality_id);