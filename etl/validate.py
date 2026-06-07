from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_SAMPLE = Path(__file__).resolve().parent / "data" / "yellow_taxi_sample.csv"


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Run a quick data quality check on the taxi sample.")
	parser.add_argument("--input", type=Path, default=DEFAULT_SAMPLE, help="CSV file to validate")
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	frame = pd.read_csv(args.input)

	print("=== Shape ===")
	print(frame.shape)

	print("\n=== Null counts ===")
	print(frame.isnull().sum())

	print("\n=== Bad fares (should be 0) ===")
	if "fare_amount" in frame.columns:
		print(f"Negative fares: {(frame['fare_amount'] < 0).sum()}")
	else:
		print("Negative fares: n/a")
	if "total_amount" in frame.columns:
		print(f"Zero total:     {(frame['total_amount'] <= 0).sum()}")
	else:
		print("Zero total:     n/a")

	print("\n=== Date range ===")
	date_column = None
	for candidate in ("tpep_pickup_datetime", "pickup_datetime"):
		if candidate in frame.columns:
			date_column = candidate
			break

	if date_column is None:
		print("Date range: n/a")
	else:
		frame[date_column] = pd.to_datetime(frame[date_column], errors="coerce")
		print(frame[date_column].min(), "→", frame[date_column].max())

	print("\n=== Payment types ===")
	if "payment_type" in frame.columns:
		print(frame["payment_type"].value_counts(dropna=False))
	else:
		print("payment_type column is missing")


if __name__ == "__main__":
	main()
