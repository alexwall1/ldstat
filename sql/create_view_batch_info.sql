create view batch_info as
select
    b.id as batch_id,
    count(bp.post_id) as num_posts,
    sum(case when p.num_jobs is not null then p.num_jobs else 0 end) as num_jobs,
    b.start_time as start_time,
    case when b.end_time is not null then b.end_time - b.start_time else null end as execution_time,
    b.complete as complete
from
    batch as b inner join
    batch_post as bp on b.id = bp.batch_id inner join
    post as p on bp.post_id = p.id
group by
    b.id,
    b.start_time,
    execution_time,
    complete
