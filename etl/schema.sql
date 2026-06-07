CREATE TABLE IF NOT EXISTS nyc_taxi.bronze_trips
(
    pickup_datetime DateTime,
    dropoff_datetime DateTime,
    passenger_count Int32,
    trip_distance Float64,
    fare_amount Float64,
    tip_amount Float64,
    total_amount Float64,
    payment_type LowCardinality(String),
    pickup_location_id Nullable(Int32),
    dropoff_location_id Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY (pickup_datetime, dropoff_datetime);