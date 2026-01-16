-- This test should return 0 rows to pass

SELECT
    f.message_id,
    d.full_date
FROM analytics.fct_messages f
JOIN analytics.dim_dates d
    ON f.date_key = d.date_key
WHERE d.full_date > CURRENT_DATE
