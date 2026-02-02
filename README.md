# 🛡️ Safe Yield Stock Bot
> **Automated Income Generation via Conservative Covered Calls**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular, automated system designed for long-term investors to generate consistent income. This bot prioritizes **capital preservation** and **share retention** by targeting low-probability strikes.

---

## 📈 Strategy
The "Safe Yield" approach is built on three unbreakable rules:
1. **Never Sell:** Strikes are selected to minimize the probability of assignment.
2. **Safety First:** Targets the **0.15 – 0.20 Delta** range.
3. **Theta Optimized:** Scans for expirations ~30 days out to capture maximum time decay.

---

## 🏗️ Architecture
The system is split into specialized modules for maximum reliability:

| Module | Responsibility |
| :--- | :--- |
| `calculators.py` | Black-Scholes & Delta probability logic. |
| `scanner.py` | Fetches live market data from Yahoo Finance. |
| `engine.py` | Coordinates the scan and generates reports. |
| `trades.csv` | A local ledger of all active and past trades. |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ and a Virtual Environment set up on your NUC.

### 2. Installation
```bash
git clone https://github.com/your-username/safe-yield-stock-bot.git
cd safe-yield-stock-bot
pip install -r requirements.txt
```

### 3. Configuration
Create a .env file in the root directory (this file is hidden from Git):
```
GOOGLE_API_KEY=your_gemini_api_key_here
MY_STOCKS=AAPL,TSLA,MSFT,SCHD
MIN_DELTA=0.15
MAX_DELTA=0.20
```

### 4. Run the Scan
Execute the engine module to generate your daily report:

```
python3 -m src.engine
```

## 📋 Roadmap
- [x] **Modular Python Architecture**: Clean separation of math and logic.
- [x] **Live Delta Scanning**: Real-time 0.15 - 0.20 strike identification.
- [ ] **AI Smart Parser**: Paste raw broker text into Telegram to log trades.
- [ ] **Telegram Alerts**: Real-time "Roll" notifications if Delta > 0.25.


