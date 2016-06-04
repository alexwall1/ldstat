alter table post
    add column professional_area_id int,
    add column professional_group_id int,
    add column county_id int;

update
    post
set
    county_id = c.id
from
    municipality as m inner join
    county as c on m.county_id = c.id
where
    post.municipality_id = m.id and post.county_id is null;


update
    post
set
    professional_group_id = pg.id
from
    professional_group as pg inner join
    profession as p on p.professional_group_id = pg.id
where
    post.profession_id = p.id and post.professional_group_id is null;


update
    post
set
    professional_area_id = pa.id
from
    professional_area as pa inner join
    professional_group as pg on pg.professional_area_id = pa.id inner join
    profession as p on p.professional_group_id = pg.id
where
    post.profession_id = p.id and post.professional_area_id is null;