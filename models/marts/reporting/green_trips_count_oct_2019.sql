select count(*) as green_trips_count_oct_2019
from {{ ref('fct_trips') }}
where service_type = 'Green'
    and pickup_datetime >= '2019-10-01' and pickup_datetime < '2019-11-01'
