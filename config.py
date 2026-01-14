import os


# Берём токен ИЗ BOT_TOKEN (как у тебя в Railway)
# или из TELEGRAM_TOKEN (если вдруг задашь так)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("BOT_TOKEN (or TELEGRAM_TOKEN) is not set")


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


ADMIN_ID = os.getenv("ADMIN_ID")
ADMIN_ID = int(ADMIN_ID) if ADMIN_ID and ADMIN_ID.isdigit() else None
