from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import clickhouse_connect
import pandas as pd

try:
	import pyarrow.parquet as pq
except ImportError:  # pragma: no cover - optional until parquet path is used
	pq = None


CH_HOST = os.environ.get("CH_HOST", "")
CH_PORT = int(os.environ.get("CH_PORT", "8443"))
CH_USER = os.environ.get("CH_USER", "default")
CH_PASSWORD = os.environ.get("CH_PASSWORD", "")
CH_DATABASE = os.environ.get("CH_DATABASE", "nyc_taxi")
CH_TABLE = os.environ.get("CH_TABLE", "bronze_trips")
CHUNK_SIZE = 10_000


parser = argparse.ArgumentParser(description="Load NYC Taxi CSV into ClickHouse")
parser.add_argument("--source", required=True, help="Path to the CSV or Parquet file")
parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE, help="Rows per batch when reading the source file")
args = parser.parse_args()


CSV_PATH = args.source


if not CH_HOST or not CH_PASSWORD:
	print("ERROR: CH_HOST and CH_PASSWORD environment variables must be set.")
	sys.exit(1)


if not os.path.exists(CSV_PATH):
	print(f"ERROR: File not found: {CSV_PATH}")
	sys.exit(1)


print(f"Connecting to ClickHouse at {CH_HOST}...")
client = clickhouse_connect.get_client(
	host=CH_HOST,
	port=CH_PORT,
	user=CH_USER,
	password=CH_PASSWORD,
	secure=True,
)
print("Connected.")


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
	out = pd.DataFrame()

	# Datetimes
	pickup_col = "tpep_pickup_datetime" if "tpep_pickup_datetime" in df.columns else "pickup_datetime"
	dropoff_col = "tpep_dropoff_datetime" if "tpep_dropoff_datetime" in df.columns else "dropoff_datetime"
	
	out["pickup_datetime"] = pd.to_datetime(df[pickup_col], errors="coerce")
	out["dropoff_datetime"] = pd.to_datetime(df[dropoff_col], errors="coerce")

	# Numerics
	out["passenger_count"] = pd.to_numeric(df["passenger_count"], errors="coerce").fillna(1).astype(int)
	out["trip_distance"] = pd.to_numeric(df["trip_distance"], errors="coerce").fillna(0)
	out["fare_amount"] = pd.to_numeric(df["fare_amount"], errors="coerce").fillna(0)
	out["tip_amount"] = pd.to_numeric(df["tip_amount"], errors="coerce").fillna(0)
	out["total_amount"] = pd.to_numeric(df["total_amount"], errors="coerce").fillna(0)

	# Payment type
	if pd.api.types.is_numeric_dtype(df["payment_type"]) or (len(df) > 0 and str(df["payment_type"].iloc[0]).isdigit()):
		payment_map = {"1": "Credit card", "2": "Cash", "3": "No charge", "4": "Dispute"}
		out["payment_type"] = (
			df["payment_type"].fillna(0).astype(int).astype(str)
			.map(payment_map).fillna("Other")
		)
	else:
		out["payment_type"] = df["payment_type"].fillna("Other")

	# Location IDs — 2015 file has lat/lon instead, so fill with 0
	out["pickup_location_id"] = 0
	out["dropoff_location_id"] = 0

	# Drop bad rows
	out = out.dropna(subset=["pickup_datetime", "dropoff_datetime"])
	out = out[(out["total_amount"] > 0) & (out["trip_distance"] > 0)]
	return out


def iter_source_frames(path: str, chunk_size: int):
	if path.lower().endswith(".parquet"):
		if pq is None:
			print("ERROR: pyarrow is required to read Parquet files. Run: pip install pyarrow")
			sys.exit(1)
		parquet_file = pq.ParquetFile(path)
		for batch in parquet_file.iter_batches(batch_size=chunk_size):
			yield batch.to_pandas()
	else:
		for chunk in pd.read_csv(path, chunksize=chunk_size):
			yield chunk


# --- Run ingestion ---
print(f"Loading from: {CSV_PATH}")
print(f"Target table: {CH_DATABASE}.{CH_TABLE}")
print("-" * 40)

total_rows = 0
for chunk in iter_source_frames(CSV_PATH, args.chunk_size):
	cleaned = clean_chunk(chunk)
	if cleaned.empty:
		continue
	client.insert_df(
		f"{CH_DATABASE}.{CH_TABLE}",
		cleaned,
		column_names=list(cleaned.columns),
	)
	total_rows += len(cleaned)
	print(f"  Inserted {total_rows:,} rows...")

print("-" * 40)
print(f"Done. {total_rows:,} rows loaded into ClickHouse.")
