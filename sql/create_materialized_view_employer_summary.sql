create materialized view employer_summary as
select
    count(p.id) as num_posts,
    sum(case when p.num_jobs is not null then p.num_jobs else 0 end) as num_jobs,
    count(distinct(c.id)) as num_counties,
    count(distinct(pa.id)) as num_professional_areas,
    p.match_data->>'arbetsplatsnamn' as employer_name,
    bp.batch_id as batch_id
from
    post as p inner join
    municipality as m on p.municipality_id = m.id inner join
    county as c on m.county_id = c.id inner join
    profession as pr on p.profession_id = pr.id inner join
    professional_group as pg on pr.professional_group_id = pg.id inner join
    professional_area as pa on pg.professional_area_id = pa.id inner join
    batch_post as bp on bp.post_id = p.id
where
    batch_id = (select max(id) from batch)
group by
    employer_name,
    batch_id
order by
    num_posts
desc