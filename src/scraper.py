import os
import json
import logging
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
from dotenv import load_dotenv

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "medical_scraper")

# --------------------------------------------------
# Directories
# --------------------------------------------------
BASE_MSG_DIR = "data/raw/telegram_messages"
BASE_IMG_DIR = "data/raw/images"
LOG_DIR = "logs"

os.makedirs(BASE_MSG_DIR, exist_ok=True)
os.makedirs(BASE_IMG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    filename=f"{LOG_DIR}/scraper.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------------------------------------
# Channels to scrape
# --------------------------------------------------
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    "tenamereja",
    "Thequorachannel"
]

# --------------------------------------------------
# Telegram client
# --------------------------------------------------
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# --------------------------------------------------
# Scrape one channel
# --------------------------------------------------
async def scrape_channel(channel_username):
    logging.info(f"Scraping channel: {channel_username}")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    msg_dir = f"{BASE_MSG_DIR}/{today}"
    img_dir = f"{BASE_IMG_DIR}/{channel_username}"

    os.makedirs(msg_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    messages = []

    channel = await client.get_entity(channel_username)

    # -----------------------------
    # STEP 1: Scrape messages
    # -----------------------------
    async for msg in client.iter_messages(channel, limit=300):
        messages.append({
            "message_id": msg.id,
            "channel_name": channel_username,
            "message_date": msg.date.isoformat() if msg.date else None,
            "message_text": msg.message,
            "views": msg.views,
            "forwards": msg.forwards,
            "has_media": bool(msg.media),
            "image_path": None
        })

    # -----------------------------
    # STEP 2: Scrape photos (limit = 100)
    # -----------------------------
    photo_count = 0
    async for msg in client.iter_messages(
        channel,
        filter=InputMessagesFilterPhotos
    ):
        if photo_count >= 50:
            break

        image_path = f"{img_dir}/{msg.id}.jpg"
        await msg.download_media(file=image_path)
        photo_count += 1

    # -----------------------------
    # Save JSON
    # -----------------------------
    output_file = f"{msg_dir}/{channel_username}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    logging.info(
        f"Saved {len(messages)} messages and "
        f"{photo_count} photos from {channel_username}"
    )

# --------------------------------------------------
# Main
# --------------------------------------------------
async def main():
    await client.start()
    for channel in CHANNELS:
        try:
            await scrape_channel(channel)
        except Exception as e:
            logging.error(f"Error scraping {channel}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
