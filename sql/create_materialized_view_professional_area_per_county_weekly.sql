create materialized view professional_area_per_county_weekly as
select
	pm.professional_area_id as professional_area_id,
	pm.professional_area_name as professional_area_name,
	pm.county_id as county_id,
	pm.county_name as county_name,
	sum(case when bp.batch_id = (select max(id)-1 from batch) then 1 else 0 end) as num_posts_w0,
	sum(case when bp.batch_id = (select max(id) from batch) then 1 else 0 end) as num_posts_w1,
	sum(case when bp.batch_id = (select max(id)-1 from batch) and p.num_jobs is not null then p.num_jobs else 0 end) as num_jobs_w0,
	sum(case when bp.batch_id = (select max(id) from batch) and p.num_jobs is not null then p.num_jobs else 0 end) as num_jobs_w1,
	count(distinct(bp.post_id)) as distinct_num_posts
from
	profession_cp_municipality as pm left join
	post as p on pm.profession_id = p.profession_id and pm.municipality_id = p.municipality_id inner join
	batch_post as bp on p.id = bp.post_id
where
	bp.batch_id = (select max(id) from batch) or bp.batch_id = (select max(id)-1 from batch)
group by
	pm.professional_area_id,
	pm.professional_area_name,
	pm.county_id,
	pm.county_name;