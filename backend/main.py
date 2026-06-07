from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

import clickhouse_connect
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NYC Taxi Analytics API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Connection factory — new client per request (thread-safe) ────────────────
def get_client():
    return clickhouse_connect.get_client(
        host=os.environ["CH_HOST"],
        port=int(os.environ.get("CH_PORT", "8443")),
        user=os.environ.get("CH_USER", "default"),
        password=os.environ["CH_PASSWORD"],
        secure=True,
    )


def query_rows(sql: str, parameters: dict | None = None):
    client = get_client()
    try:
        result = client.query(sql, parameters=parameters)
        return result.result_rows
    finally:
        client.close()


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/kpis")
def get_kpis():
    row = query_rows(
        """
        SELECT
            sum(total_trips)      AS total_trips,
            sum(total_revenue)    AS total_revenue,
            avg(avg_distance)     AS avg_distance,
            avg(avg_duration_min) AS avg_duration
        FROM nyc_taxi.mart_trips_daily
        """
    )[0]
    return {
        "total_trips":      int(row[0] or 0),
        "total_revenue":    round(float(row[1] or 0), 2),
        "avg_distance":     round(float(row[2] or 0), 2),
        "avg_duration_min": round(float(row[3] or 0), 1),
    }


@app.get("/api/trips-by-day")
def trips_by_day(
    start: str = Query("2015-01-01"),
    end:   str = Query("2015-01-31"),
):
    rows = query_rows(
        """
        SELECT
            pickup_date,
            sum(total_trips)   AS trips,
            sum(total_revenue) AS revenue
        FROM nyc_taxi.mart_trips_daily
        WHERE pickup_date BETWEEN {start:String} AND {end:String}
        GROUP BY pickup_date
        ORDER BY pickup_date
        """,
        {"start": start, "end": end},
    )
    return [
        {"date": str(r[0]), "trips": int(r[1] or 0), "revenue": round(float(r[2] or 0), 2)}
        for r in rows
    ]


@app.get("/api/trips-by-hour")
def trips_by_hour(
    start: str = Query("2015-01-01"),
    end:   str = Query("2015-01-31"),
):
    rows = query_rows(
        """
        SELECT
            pickup_hour,
            sum(total_trips)       AS trips,
            avg(avg_tip_pct) * 100 AS tip_pct
        FROM nyc_taxi.mart_trips_daily
        WHERE pickup_date BETWEEN {start:String} AND {end:String}
        GROUP BY pickup_hour
        ORDER BY pickup_hour
        """,
        {"start": start, "end": end},
    )
    return [
        {"hour": int(r[0]), "trips": int(r[1] or 0), "tip_pct": round(float(r[2] or 0), 1)}
        for r in rows
    ]


@app.get("/api/payment-breakdown")
def payment_breakdown(
    start: str = Query("2015-01-01"),
    end:   str = Query("2015-01-31"),
):
    rows = query_rows(
        """
        SELECT payment_method, sum(total_trips) AS trips
        FROM nyc_taxi.mart_trips_daily
        WHERE pickup_date BETWEEN {start:String} AND {end:String}
        GROUP BY payment_method
        ORDER BY trips DESC
        """,
        {"start": start, "end": end},
    )
    return [{"payment_method": r[0], "trips": int(r[1] or 0)} for r in rows]
