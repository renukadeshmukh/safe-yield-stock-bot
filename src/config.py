import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MY_STOCKS = [s.strip() for s in os.getenv("MY_STOCKS", "AAPL,TSLA,MSFT,SCHD").split(",")]
MIN_DELTA = float(os.getenv("MIN_DELTA", "0.15"))
MAX_DELTA = float(os.getenv("MAX_DELTA", "0.20"))
RISK_FREE_RATE = float(os.getenv("RISK_FREE_RATE", "0.04"))
HEALTHCHECK_URL = os.getenv("HEALTHCHECK_URL")
