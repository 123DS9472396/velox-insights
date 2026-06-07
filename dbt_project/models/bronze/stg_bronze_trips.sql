{{ config(materialized='view') }}

SELECT
	trip_id,
	pickup_datetime,
	dropoff_datetime,
	passenger_count,
	trip_distance,
	fare_amount,
	tip_amount,
	total_amount,
	payment_type,
	pickup_location_id,
	dropoff_location_id,
	ingested_at
FROM {{ source('nyc_taxi', 'bronze_trips') }}
