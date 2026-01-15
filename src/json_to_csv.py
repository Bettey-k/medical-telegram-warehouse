import json
import csv
from pathlib import Path

DATA_DIR = Path("data/raw/telegram_messages")
OUT_FILE = Path("data/raw/telegram_messages.csv")

rows = []

for date_dir in DATA_DIR.iterdir():
    if date_dir.is_dir():
        for jf in date_dir.glob("*.json"):
            with open(jf, "r", encoding="utf-8") as f:
                rows.extend(json.load(f))

with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("✅ CSV created:", OUT_FILE)
