from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TelegramClient(
    os.getenv("SESSION_NAME"),
    os.getenv("TELEGRAM_API_ID"),
    os.getenv("TELEGRAM_API_HASH")
)

with client:
    print("✅ Telegram connection successful")
