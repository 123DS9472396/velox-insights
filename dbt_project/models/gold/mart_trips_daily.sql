{{
	config(
		materialized='table',
		engine='MergeTree()',
		order_by='(pickup_date)'
	)
}}

SELECT
	pickup_date,
	pickup_hour,
	day_of_week,
	payment_method,
	count(*)               AS total_trips,
	sum(total_amount)      AS total_revenue,
	avg(trip_distance)     AS avg_distance,
	avg(trip_duration_min) AS avg_duration_min,
	avg(tip_amount / nullIf(fare_amount, 0)) AS avg_tip_pct,
	sum(passenger_count)    AS total_passengers
FROM {{ ref('int_trips_cleaned') }}
GROUP BY
	pickup_date,
	pickup_hour,
	day_of_week,
	payment_method
ORDER BY pickup_date
