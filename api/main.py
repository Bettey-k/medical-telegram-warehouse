from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from api.database import get_db
from api import schemas

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytical API built on dbt-modeled data warehouse",
    version="1.0.0"
)

# --------------------------------------------------
# Root
# --------------------------------------------------
@app.get("/")
def root():
    return {"message": "Medical Telegram Analytics API is running"}


# --------------------------------------------------
# Endpoint 1: Top Products
# --------------------------------------------------
@app.get(
    "/api/reports/top-products",
    response_model=List[schemas.TopProduct],
    summary="Top mentioned products",
    description="Returns most frequently mentioned product-related terms across all channels"
)
def top_products(
    limit: int = Query(10, gt=0, le=50),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            lower(word) AS term,
            COUNT(*) AS frequency
        FROM analytics.fct_messages,
        unnest(string_to_array(message_text, ' ')) AS word
        WHERE length(word) > 4
        GROUP BY term
        ORDER BY frequency DESC
        LIMIT :limit
    """)

    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"term": r.term, "frequency": r.frequency} for r in result]


# --------------------------------------------------
# Endpoint 2: Channel Activity
# --------------------------------------------------
@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=schemas.ChannelActivity,
    summary="Channel posting activity",
    description="Returns posting activity and average views for a specific channel"
)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            c.channel_name,
            COUNT(f.message_id) AS total_posts,
            AVG(f.view_count) AS avg_views
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c
          ON f.channel_key = c.channel_key
        WHERE c.channel_name = :channel_name
        GROUP BY c.channel_name
    """)

    row = db.execute(query, {"channel_name": channel_name}).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Channel not found")

    return {
        "channel_name": row.channel_name,
        "total_posts": row.total_posts,
        "avg_views": float(row.avg_views)
    }


# --------------------------------------------------
# Endpoint 3: Message Search
# --------------------------------------------------
@app.get(
    "/api/search/messages",
    response_model=List[schemas.MessageSearchResult],
    summary="Message search",
    description="Search for messages containing a specific term"
)
def search_messages(
    query: str = Query(..., min_length=3),
    limit: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    sql = text("""
        SELECT
            f.message_id,
            c.channel_name,
            f.message_text,
            f.view_count
        FROM analytics.fct_messages f
        JOIN analytics.dim_channels c
          ON f.channel_key = c.channel_key
        WHERE lower(f.message_text) LIKE lower(:pattern)
        ORDER BY f.view_count DESC
        LIMIT :limit
    """)

    rows = db.execute(
        sql,
        {"pattern": f"%{query}%", "limit": limit}
    ).fetchall()

    return [
        {
            "message_id": r.message_id,
            "channel_name": r.channel_name,
            "message_text": r.message_text,
            "view_count": r.view_count
        }
        for r in rows
    ]


# --------------------------------------------------
# Endpoint 4: Visual Content Stats
# --------------------------------------------------
@app.get(
    "/api/reports/visual-content",
    response_model=List[schemas.VisualContentStat],
    summary="Visual content stats",
    description="Returns visual content statistics for each channel"
)
def visual_content_stats(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            c.channel_name,
            COUNT(*) AS total_images,
            SUM(CASE WHEN image_category = 'promotional' THEN 1 ELSE 0 END) AS promotional,
            SUM(CASE WHEN image_category = 'product_display' THEN 1 ELSE 0 END) AS product_display,
            SUM(CASE WHEN image_category = 'lifestyle' THEN 1 ELSE 0 END) AS lifestyle,
            SUM(CASE WHEN image_category = 'other' THEN 1 ELSE 0 END) AS other
        FROM analytics.fct_image_detections i
        JOIN analytics.dim_channels c
          ON i.channel_key = c.channel_key
        GROUP BY c.channel_name
        ORDER BY total_images DESC
    """)

    rows = db.execute(query).fetchall()

    return [
        {
            "channel_name": r.channel_name,
            "total_images": r.total_images,
            "promotional": r.promotional,
            "product_display": r.product_display,
            "lifestyle": r.lifestyle,
            "other": r.other
        }
        for r in rows
    ]
