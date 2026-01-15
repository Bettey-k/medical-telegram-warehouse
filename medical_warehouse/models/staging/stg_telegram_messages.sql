with source as (

    select
        message_id::bigint               as message_id,
        channel_name::text               as channel_name,
        message_date::timestamp          as message_timestamp,
        message_text::text               as message_text,
        views::int                       as view_count,
        forwards::int                    as forward_count,
        has_media::boolean               as has_image

    from raw.telegram_messages

),

cleaned as (

    select
        *,
        length(message_text)             as message_length,
        date(message_timestamp)          as message_date

    from source
    where message_text is not null
      and trim(message_text) <> ''

)

select * from cleaned
