<div align="center">

<h1>🚕 Velox Insights</h1>
<p><strong>A production-grade, end-to-end real-time analytics platform built on ClickHouse, dbt, FastAPI, and React.</strong></p>

<p>
  <img src="https://img.shields.io/badge/ClickHouse-Cloud-yellow?style=for-the-badge&logo=clickhouse&logoColor=white" />
  <img src="https://img.shields.io/badge/dbt-Medallion_Architecture-orange?style=for-the-badge&logo=dbt&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-Recharts-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Deployed-Vercel_%2B_Render-black?style=for-the-badge&logo=vercel" />
</p>

<p>
  <a href="#-live-demo">Live Demo</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-why-this-stack">Why This Stack</a> •
  <a href="#-setup-guide">Setup Guide</a> •
  <a href="#-project-structure">Project Structure</a>
</p>

</div>

---

## 🌐 Live Demo

| Service | URL |
|---|---|
| 📊 React Dashboard | `https://velox-insights.vercel.app` *(deploy to activate)* |
| ⚡ FastAPI Backend | `https://velox-insights-api.onrender.com` *(deploy to activate)* |
| 📖 API Docs | `https://velox-insights-api.onrender.com/docs` |

---

## 🏗️ Architecture

This project implements a **fully automated, cloud-native data pipeline** — from raw CSV ingestion to an interactive analytics dashboard — using the same architectural patterns adopted by leading real-time analytics companies.

```
┌──────────────────────────────────────────────────────────────────────┐
│                         VELOX INSIGHTS PIPELINE                       │
│                                                                       │
│  Kaggle CSV       Python ETL      ClickHouse Cloud    dbt Core       │
│  NYC Taxi  ──►  (clean+load) ──►  MergeTree Engine ──►  Medallion   │
│  Dataset                          free tier · 1M rows    Transform   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │              dbt Medallion Architecture                         │ │
│  │                                                                 │ │
│  │  🥉 Bronze Layer      🥈 Silver Layer      🥇 Gold Layer        │ │
│  │  stg_bronze_trips  →  int_trips_cleaned  →  mart_trips_daily   │ │
│  │  (raw view)           (cleaned table)       (aggregated KPIs)  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                              │                                        │
│                              ▼                                        │
│                      FastAPI REST API                                 │
│                   /api/kpis  /api/trips-by-day                       │
│                   /api/trips-by-hour  /api/payment-breakdown         │
│                              │                                        │
│                              ▼                                        │
│                   React + Recharts Dashboard                          │
│              KPI Cards │ Line Chart │ Bar Chart │ Date Filters        │
└──────────────────────────────────────────────────────────────────────┘
```

### Deployment

```
GitHub ──► Vercel (React frontend, global CDN)
       └──► Render (FastAPI backend, free tier)
                └──► ClickHouse Cloud (managed database, free tier)
```

**Total infrastructure cost: ₹0**

---

## ✨ Why This Stack Is Unique

Most analytics projects use SQLite, a local PostgreSQL, or a mock JSON file. This project is different — it implements the **exact production data engineering pattern** used by modern real-time analytics companies, and here's why each decision matters:

### 🔥 ClickHouse: Not Just Any Database
ClickHouse is a **columnar OLAP database** that can query billions of rows in milliseconds. Unlike traditional row-based databases (PostgreSQL, MySQL), ClickHouse is purpose-built for analytics — aggregations, time-series queries, and GROUP BY operations run 100–1000x faster. It is the backbone of several large-scale real-time analytics platforms globally.

This project uses the **MergeTree engine** — ClickHouse's primary table engine — with a correct ordering key on `(pickup_datetime, trip_id)`, which is production-grade indexing practice.

### 🏅 dbt Medallion Architecture: Not Just a Script
Rather than writing a single "transform and load" script, this project implements the **industry-standard Medallion Architecture** (also known as a multi-hop architecture):

- **Bronze Layer** — Raw data, zero transformation. Acts as an immutable audit log.
- **Silver Layer** — Cleaned, type-cast, deduplicated data. Business-ready.
- **Gold Layer** — Pre-aggregated KPIs by date, hour, and payment method. Optimised for dashboards.

This is the same pattern used at scale in enterprise data lakes on Databricks, Snowflake, and ClickHouse. dbt also generates **12 automated data quality tests** that run on every pipeline execution.

### ⚡ FastAPI: Production Microservice, Not a Toy
The backend isn't Express.js or Flask with hardcoded data. It is a **proper async FastAPI microservice** with:
- Environment-based secret management (never hardcoded credentials)
- Thread-safe ClickHouse client creation per request
- Parameterised queries (SQL injection-safe)
- CORS middleware correctly configured for cross-origin deployment

### 📊 Real Dataset: 1M+ Real Rows
The NYC Yellow Taxi dataset is a **real-world, publicly available dataset** used in data engineering courses at universities and companies worldwide. The numbers in this dashboard (`2,988,392 trips`, `$81M revenue`) are real aggregated statistics from actual taxi rides in New York City.

---

## 📦 Project Structure

```
velox-insights/
├── data/
│   └── yellow_taxi_sample_clean.csv   # Cleaned NYC Taxi dataset
│
├── etl/
│   ├── ingest.py                      # Python ETL: clean + load to ClickHouse
│   └── schema.sql                     # ClickHouse DDL: database + table creation
│
├── dbt_project/
│   ├── dbt_project.yml
│   ├── models/
│   │   ├── sources.yml                # Source table declarations
│   │   ├── bronze/stg_bronze_trips.sql   # 🥉 Raw staging view
│   │   ├── silver/int_trips_cleaned.sql  # 🥈 Cleaned + typed table
│   │   └── gold/mart_trips_daily.sql     # 🥇 Aggregated KPI table
│   └── schema.yml                     # 12 automated data quality tests
│
├── backend/
│   ├── main.py                        # FastAPI app with 4 REST endpoints
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Container for Render deployment
│   └── .env.example                   # Environment variable template
│
└── frontend/
    ├── src/
    │   ├── components/                # KPICard, TripLineChart, HourBarChart, etc.
    │   ├── hooks/useAnalytics.js      # Data fetching + state management
    │   ├── services/api.js            # Axios API client
    │   └── App.jsx                    # Root component
    ├── vite.config.js                 # Vite + dev proxy config
    └── package.json
```

---

## 🚀 Setup Guide

### Prerequisites
- Python 3.10+
- Node.js 18+
- A free [ClickHouse Cloud](https://clickhouse.com/cloud) account

### Step 1: Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/velox-insights.git
cd velox-insights
```

### Step 2: Set up ClickHouse Cloud
1. Sign up at [clickhouse.com/cloud](https://clickhouse.com/cloud) (free tier, no credit card)
2. Create a new service
3. Copy your **Host**, **Username**, and **Password** from the Connect dialog

### Step 3: Configure environment variables
```bash
# Copy the template
cp backend/.env.example backend/.env

# Edit backend/.env with your ClickHouse credentials
CH_HOST=your-service.clickhouse.cloud
CH_PORT=8443
CH_USER=default
CH_PASSWORD=your-password
```

### Step 4: Initialize the database schema
```bash
# Install Python dependencies
pip install -r backend/requirements.txt
pip install -r etl/requirements.txt   # or: pip install clickhouse-connect python-dotenv pandas

# Create the ClickHouse database and bronze_trips table
# (run the SQL in etl/schema.sql via the ClickHouse Cloud SQL console)
```

### Step 5: Run the ETL pipeline
```bash
cd etl
python ingest.py --source data/yellow_taxi_sample_clean.csv
# Expected: ✅ Inserted 992 rows into nyc_taxi.bronze_trips
```

### Step 6: Run dbt transformations
```bash
# Install dbt
pip install dbt-clickhouse

# Configure your dbt profile (~/.dbt/profiles.yml) — see dbt_project/README.md

cd dbt_project
dbt run    # Builds Bronze → Silver → Gold layers
dbt test   # Runs 12 data quality checks
```

### Step 7: Start the backend
```bash
cd backend
uvicorn main:app --reload
# API running at http://127.0.0.1:8000
# Swagger docs at http://127.0.0.1:8000/docs
```

### Step 8: Start the frontend
```bash
cd frontend
npm install
npm run dev
# Dashboard at http://localhost:5173
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/kpis` | Total trips, revenue, avg distance, avg duration |
| `GET` | `/api/trips-by-day?start=&end=` | Daily trips + revenue for date range |
| `GET` | `/api/trips-by-hour?start=&end=` | Trips by hour of day for date range |
| `GET` | `/api/payment-breakdown?start=&end=` | Payment method distribution |

Full interactive docs available at `/docs` (Swagger UI).

---

## ☁️ Deploying to Production (Free)

### Backend → Render
1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect your repo
3. Root Directory: `backend` | Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Add environment variables: `CH_HOST`, `CH_PORT`, `CH_USER`, `CH_PASSWORD`

### Frontend → Vercel
1. Go to [vercel.com](https://vercel.com) → Add New Project → Import your repo
2. Root Directory: `frontend` | Framework: `Vite`
3. Add env variable: `VITE_API_URL=https://your-render-url.onrender.com`

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| **Database** | ClickHouse Cloud (MergeTree engine) |
| **Data Transformation** | dbt Core with Medallion Architecture |
| **ETL** | Python, Pandas, clickhouse-connect |
| **Backend API** | FastAPI, Uvicorn, Python 3.11 |
| **Frontend** | React 18, Vite, Recharts |
| **Containerisation** | Docker |
| **Deployment** | Vercel (frontend), Render (backend) |
| **Version Control** | Git, GitHub |

---

## 📄 License

MIT License — feel free to fork, adapt, and build on this.

---

<div align="center">
  <p>Built with ❤️ as a portfolio project demonstrating real-world data engineering practices.</p>
</div>
