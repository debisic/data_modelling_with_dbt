-- Best performing pickup zone for Green taxi in 2020 by total revenue
-- Aggregates monthly revenue data to find the highest earning zone for green taxis

SELECT
    pickup_zone,
    sum(revenue_monthly_total_amount) as total_revenue_2020,
    sum(total_monthly_trips) as total_trips,
    sum(avg_monthly_passenger_count * total_monthly_trips) / nullif(sum(total_monthly_trips), 0) as avg_passenger_count,
    sum(avg_monthly_trip_distance * total_monthly_trips) / nullif(sum(total_monthly_trips), 0) as avg_trip_distance
from {{ ref('fct_monthly_zone_revenue') }}
where service_type = 'Green'
    and date_part('year', revenue_month) = 2020
group by pickup_zone
order by total_revenue_2020 desc
Limit 3
