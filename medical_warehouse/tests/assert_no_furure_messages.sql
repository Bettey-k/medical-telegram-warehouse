-- This test fails if any message has a future date

SELECT *
FROM {{ ref('fct_messages') }}
WHERE message_date > CURRENT_DATE
