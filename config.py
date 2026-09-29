import os
from dotenv import load_dotenv

load_dotenv()

try:
    TG_API_ID = int(os.getenv("38315480", "0"))
except ValueError:
    TG_API_ID = 0

TG_API_HASH = os.getenv("c2da649e07e13bf8d3b4b8c7b9fef057", "")
TG_PHONE = os.getenv("+855 96 252 5463", "")

OPENAI_API_KEY = os.getenv("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", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

try:
    OWNER_ID = int(os.getenv("8736435737", "0"))
except ValueError:
    OWNER_ID = 0

AUTO_REPLY = os.getenv("AUTO_REPLY", "true").lower() == "true"

REPLY_DELAY = float(os.getenv("REPLY_DELAY", "2"))
OWNER_PAUSE_SECONDS = int(
    os.getenv("OWNER_PAUSE_SECONDS", "60")
)

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "20"))
