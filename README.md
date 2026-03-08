# 🛡️ Safe Yield Stock Bot

> **Automated Income Generation via Conservative Covered Calls**

![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![CI/CD](https://github.com/renukadeshmukh/safe-yield-stock-bot/actions/workflows/ci-cd.yml/badge.svg)

A modular, automated system designed for long-term investors to generate consistent income. This bot prioritizes **capital preservation** and **share retention** by targeting low-probability strikes.

## 📈 Strategy: The "Income Harvest"

### 1. Covered Calls (Income Generation)
* **Goal:** Sell OTM calls to collect premium.
* **"Never Sell" Rule:** Target **0.15 - 0.20 Delta** (~80-85% probability of keeping shares).

### 2. Cash Secured Puts (Entry/Acquisition)
* **Goal:** Sell puts on high-quality stocks at prices we're happy to own.

### 3. Risk Management & Rolling
* **Delta Monitoring:** If Delta drifts toward 0.25+, flag for a "Roll" to avoid assignment.

## 🏗️ Architecture

```
safe-yield-stock-bot/
├── src/
│   ├── config.py                  # .env config loading
│   ├── engine.py                  # Main entrypoint
│   ├── core/
│   │   ├── calculators.py         # Black-Scholes delta math
│   │   └── prorate.py             # Premium pro-rating across months
│   ├── strategy/
│   │   └── scanner.py             # Option chain scanner (Yahoo Finance)
│   └── integrations/
│       ├── nlp_parser.py          # Gemini-powered trade text parser
│       └── telegram_bot.py        # Two-way Telegram messaging
├── tests/
│   ├── test_nlp_parser.py
│   ├── test_prorate.py
│   └── test_telegram_bot.py
├── .github/workflows/ci-cd.yml   # GitHub Actions CI/CD
├── Dockerfile                     # Containerized deployment
├── run_telegram.py                # Standalone Telegram bot runner
└── requirements.txt
```

### Module Responsibilities

| Module | Layer | Responsibility |
|--------|-------|----------------|
| `calculators.py` | Core | Black-Scholes & Delta probability logic |
| `prorate.py` | Core | Premium pro-rating across calendar months |
| `scanner.py` | Strategy | Fetches live options data, filters by delta range |
| `nlp_parser.py` | Integrations | LLM extraction of trade details from brokerage text |
| `telegram_bot.py` | Integrations | Two-way Telegram: alerts out, trade text in |

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.13+
- Gemini API key (free) — [Get one here](https://aistudio.google.com/apikey)
- Telegram bot token — [Create via BotFather](https://t.me/BotFather)

### 2. Installation

```bash
git clone https://github.com/renukadeshmukh/safe-yield-stock-bot.git
cd safe-yield-stock-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_API_KEY=your_gemini_api_key
MY_STOCKS=AAPL,TSLA,MSFT,SCHD
MIN_DELTA=0.15
MAX_DELTA=0.20
RISK_FREE_RATE=0.04
```

### 4. Run

```bash
# Option scanner report
python -m src.engine

# Telegram bot (interactive)
python run_telegram.py
```

### 5. Run Tests

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

## 🔄 CI/CD Pipeline

Every push to `main` triggers:

```
git push → GitHub Actions → pytest → Docker build → Push to GHCR → Deploy to NUC
```

- **Tests gate deployment** — if tests fail, nothing deploys
- **Docker-based** — code + deps baked into image, no "works on my machine"
- **Auto-restart** — container restarts on crash

## 📋 Roadmap

- [x] Black-Scholes delta scanning
- [x] .env-based configuration
- [x] NLP trade parser (Gemini)
- [x] Premium pro-rating logic
- [x] Telegram bot (two-way)
- [x] CI/CD pipeline (GitHub Actions + Docker)
- [ ] Google Sheets integration (trade ledger + dashboard)
- [ ] Sentiment analysis (news headlines)
- [ ] Earnings date alerts
- [ ] Decision engine ("Guardian" — profit take, roll, sentiment triggers)
- [ ] 15-minute heartbeat scheduler
- [ ] MCP server (expose tools for AI agent consumption)
- [ ] Agno agent integration

## License

MIT
