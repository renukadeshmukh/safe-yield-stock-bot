import json
import google.generativeai as genai
from .config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)
_model = genai.GenerativeModel("gemini-1.5-flash")

EXTRACTION_PROMPT = """Extract trade details from this brokerage text. Return ONLY valid JSON:
{
  "ticker": "AAPL",
  "action": "SELL_TO_OPEN",
  "quantity": 1,
  "strike": 230.0,
  "expiry": "2026-04-18",
  "premium": 3.45
}

Rules:
- action must be one of: SELL_TO_OPEN, BUY_TO_CLOSE, SELL_TO_CLOSE, BUY_TO_OPEN
- premium is per-share (not per-contract)
- expiry in YYYY-MM-DD format
- If a field cannot be determined, use null

Brokerage text:
"""


def parse_trade(raw_text: str) -> dict | None:
    """Parse raw brokerage text into structured trade data via Gemini."""
    response = _model.generate_content(EXTRACTION_PROMPT + raw_text)
    try:
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return None
