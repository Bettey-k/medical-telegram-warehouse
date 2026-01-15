with base as (

    select
        channel_name,
        min(message_date)        as first_post_date,
        max(message_date)        as last_post_date,
        count(*)                 as total_posts,
        avg(view_count)          as avg_views
    from analytics.stg_telegram_messages
    group by channel_name

),

final as (

    select
        row_number() over (order by channel_name) as channel_key,
        channel_name,
        case
            when lower(channel_name) like '%pharma%' then 'Pharmaceutical'
            when lower(channel_name) like '%cosmetic%' then 'Cosmetics'
            else 'Medical'
        end as channel_type,
        first_post_date,
        last_post_date,
        total_posts,
        round(avg_views, 2) as avg_views
    from base

)

select * from final
