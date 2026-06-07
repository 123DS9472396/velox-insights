{{
	config(
		materialized='table',
		engine='MergeTree()',
		order_by='(pickup_date, trip_id)'
	)
}}

SELECT
	trip_id,
	pickup_datetime,
	dropoff_datetime,
	toDate(pickup_datetime)                               AS pickup_date,
	toHour(pickup_datetime)                               AS pickup_hour,
	toDayOfWeek(pickup_datetime)                          AS day_of_week,
	dateDiff('minute', pickup_datetime, dropoff_datetime) AS trip_duration_min,
	passenger_count,
	trip_distance,
	fare_amount,
	tip_amount,
	total_amount,
	CASE
		WHEN payment_type IN ('1', '1.0', 'Credit card') THEN 'Credit card'
		WHEN payment_type IN ('2', '2.0', 'Cash') THEN 'Cash'
		WHEN payment_type IN ('3', '3.0', 'No charge') THEN 'No charge'
		WHEN payment_type IN ('4', '4.0', 'Dispute') THEN 'Dispute'
		ELSE payment_type
	END AS payment_method
FROM {{ ref('stg_bronze_trips') }}
WHERE dateDiff('minute', pickup_datetime, dropoff_datetime) BETWEEN 1 AND 180
  AND trip_distance BETWEEN 0.1 AND 100
  AND total_amount BETWEEN 1 AND 500
