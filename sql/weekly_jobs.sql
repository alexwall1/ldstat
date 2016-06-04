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

refresh materialized view employer_summary;
--- refresh materialized view professional_area_weekly;
--- refresh materialized view county_weekly;
--- refresh materialized view distinct_num_posts_per_week_and_county;
--- refresh materialized view distinct_num_posts_per_week_and_professional_area;
refresh materialized view distinct_num_posts_per_county_professional_area_week;
refresh materialized view distinct_num_posts_per_county_professional_group_week;

--copy (select
--        start_time,
--        professional_area_name,
--        sum(distinct_num_posts) as distinct_num_posts
--    from
--        distinct_posts_per_county_professional_area_week
--    group by
--        professional_area_name,
--        start_time
--    order by
--        professional_area_name,
--        start_time) to '/home/alexwall/webapps/demo/ldstat/ldstat/static/csv/dump.csv' with CSV DELIMITER ';' HEADER ENCODING 'iso-8859-1';
