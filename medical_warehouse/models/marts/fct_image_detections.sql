{{ config(materialized='table') }}

WITH detections AS (
    SELECT
        message_id,
        detected_objects,
        avg_confidence,
        image_category
    FROM raw.image_detections_raw
),

messages AS (
    SELECT
        message_id,
        channel_key,
        date_key
    FROM analytics.fct_messages
)

SELECT
    d.message_id,
    m.channel_key,
    m.date_key,
    d.detected_objects,
    d.avg_confidence AS confidence_score,
    d.image_category
FROM detections d
LEFT JOIN messages m
    ON d.message_id = m.message_id
