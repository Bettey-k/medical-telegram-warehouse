🏥 Medical Telegram Analytics Pipeline

An end-to-end data engineering & analytics pipeline that ingests Telegram data, transforms it into a dimensional data warehouse, enriches it with computer vision, exposes analytical insights via an API, and orchestrates the entire workflow using Dagster.

📌 Project Overview

This project analyzes medical-related Telegram channels to extract insights about:

Product mentions and engagement

Channel activity and trends

Visual content usage (images)

Promotional vs non-promotional posts

The pipeline follows modern data engineering best practices:

Data Lake → Data Warehouse → Analytics API → Orchestration
Telegram Scraper
        │
        ▼
Data Lake (JSON files)
        │
        ▼
PostgreSQL (raw schema)
        │
        ▼
dbt Transformations
(staging + star schema)
        │
        ▼
YOLO Image Enrichment
        │
        ▼
Analytics Data Mart
        │
        ▼
FastAPI Analytical API
        │
        ▼
Dagster Orchestration

📂 Project Structure
medical-telegram-warehouse/
├── api/                       # FastAPI application
│   ├── main.py
│   ├── database.py
│   └── schemas.py
├── data/
│   └── raw/
│       └── telegram_messages/
├── medical_warehouse/         # dbt project
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
├── src/
│   ├── scrape_telegram.py
│   ├── load_raw_to_postgres.py
│   └── yolo_detect.py
├── pipeline.py                # Dagster pipeline
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
Task Breakdown
✅ Task 1 – Data Scraping

Goal: Collect Telegram messages and media
Output: JSON files stored in a data lake structure

Scrapes messages and images from medical Telegram channels

Stores data in date-partitioned folders

Handles malformed or empty messages safely

📁 Example:
data/raw/telegram_messages/2026-01-15/messages.json

ask 2 – Data Modeling & Transformation (dbt)

Goal: Build a trusted analytical data warehouse

Raw Layer

raw.telegram_messages

Staging Layer

stg_telegram_messages

Cleaned fields

Type casting

Calculated features (message length, image flag)

Data Marts (Star Schema)
Dimensions

dim_channels

dim_dates

Fact Tables

fct_messages

Data Quality

not_null, unique, relationships tests

Custom tests:

No future-dated messages

Non-negative view counts

✅ Task 3 – Data Enrichment with YOLO

Goal: Analyze images using computer vision

Uses YOLOv8 nano

Detects general objects (person, bottle, phone, etc.)

Classifies images into:

promotional

product_display

lifestyle

other

Output

yolo_detections.csv

Integrated into warehouse as:

fct_image_detections

✅ Task 4 – Analytical API (FastAPI)

Goal: Expose insights via REST API

Available Endpoints
Endpoint	Description
/api/reports/top-products	Most mentioned product terms
/api/channels/{channel}/activity	Channel activity metrics
/api/search/messages	Keyword-based message search
/api/reports/visual-content	Image usage statistics
Features

SQLAlchemy integration

Pydantic validation

Auto-generated docs

📖 API Docs:
http://127.0.0.1:8000/docs
✅ Task 5 – Pipeline Orchestration (Dagster)

Goal: Automate and monitor the full pipeline

Pipeline Ops

scrape_telegram_data

load_raw_to_postgres

run_dbt_transformations

run_yolo_enrichment

Key Design Choices

Defensive execution for scraping & YOLO

Clear logging and failure isolation

Daily scheduling support

Dagster UI
http://localhost:3000

Docker & Deployment
Build & Run Everything

docker compose up --build
Services

PostgreSQL

Dagster webserver

Pipeline execution environment

⚙️ Environment Variables

Create a .env file:
DATABASE_URL=postgresql+psycopg2://postgres:@medical_postgres:5432/medical_dw

Key Insights (Example)

Promotional posts tend to receive higher engagement

Certain channels rely heavily on visual content

Pre-trained YOLO models struggle with domain-specific medical products

🧠 Limitations

YOLO is not trained on medical products

Telegram scraping depends on external access

Image enrichment is computationally expensive

🚀 Future Improvements

Custom object detection model

Incremental dbt models

API caching and pagination

Cloud deployment (AWS/GCP)

🧾 How to Run Locally (Without Docker)

# Load raw data
python src/load_raw_to_postgres.py

# Run dbt
cd medical_warehouse
dbt run
dbt test

# Start API
uvicorn api.main:app --reload

# Start Dagster
dagster dev -f pipeline.py

Final Notes

This project demonstrates:

Modern data engineering architecture

Dimensional modeling

Automated orchestration

Production-ready analytics exposure

✅ All tasks completed successfully