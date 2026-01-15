import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:@localhost:5432/medical_dw"
)

RAW_BASE_PATH = "data/raw/telegram_messages"

def load_json_files():
    records = []

    if not os.path.exists(RAW_BASE_PATH):
        print(f"❌ Path not found: {RAW_BASE_PATH}")
        return pd.DataFrame()

    for date_folder in os.listdir(RAW_BASE_PATH):
        date_path = os.path.join(RAW_BASE_PATH, date_folder)

        if not os.path.isdir(date_path):
            continue

        for file in os.listdir(date_path):
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(date_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    records.extend(data)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON: {file_path}")

    return pd.DataFrame(records)

def main():
    print(f"Using DATABASE_URL: {DATABASE_URL}")
    print("Loading raw Telegram JSON files...")

    df = load_json_files()

    print(f"Loaded {len(df)} records")

    if df.empty:
        print("⚠️ No data found. Check the folder structure.")
        return

    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    print("Writing to raw.telegram_messages...")

    df.to_sql(
        "telegram_messages",
        engine,
        schema="raw",
        if_exists="replace",
        index=False,
        method="multi"
    )

    print("✅ Data loaded successfully into raw.telegram_messages")

if __name__ == "__main__":
    main()
