create materialized view professional_group_per_municipality_weekly as
select
	pm.professional_group_id as professional_group_id,
	pm.professional_group_name as professional_group_name,
	pm.municipality_id as municipality_id,
	pm.municipality_name as municipality_name,
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
	pm.professional_group_id,
	pm.professional_group_name,
	pm.municipality_id,
	pm.municipality_name;