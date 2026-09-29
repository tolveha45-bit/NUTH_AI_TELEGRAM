import os
from dotenv import load_dotenv

load_dotenv()
try:
    TG_API_ID = int(os.getenv("TG_API_ID", "0"))
except ValueError:
    TG_API_ID = 0
TG_API_HASH = os.getenv("TG_API_HASH", "")
TG_PHONE = os.getenv("TG_PHONE", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

AUTO_REPLY = os.getenv("AUTO_REPLY", "true").lower() == "true"

REPLY_DELAY = float(os.getenv("REPLY_DELAY", "2"))
OWNER_PAUSE_SECONDS = int(
    os.getenv("OWNER_PAUSE_SECONDS", "60")
)

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))
