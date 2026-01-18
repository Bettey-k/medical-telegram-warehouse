from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    term: str
    frequency: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_posts: int
    avg_views: float

class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    view_count: int

class VisualContentStat(BaseModel):
    channel_name: str
    total_images: int
    promotional: int
    product_display: int
    lifestyle: int
    other: int
