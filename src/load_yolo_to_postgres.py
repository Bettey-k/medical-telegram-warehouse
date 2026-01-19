import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:@localhost:5432/medical_dw"
)

engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/yolo_detections.csv")

df.to_sql(
    "image_detections_raw",
    engine,
    schema="raw",
    if_exists="replace",
    index=False
)

print("✅ YOLO detections loaded into raw.image_detections_raw")
