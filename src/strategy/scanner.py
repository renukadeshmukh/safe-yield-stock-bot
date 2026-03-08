import yfinance as yf
from datetime import datetime
from ..core.calculators import calculate_delta
from ..config import MIN_DELTA, MAX_DELTA, RISK_FREE_RATE


def find_safe_options(symbol, target_delta_min=None, target_delta_max=None):
    """
    Connects to Yahoo Finance and filters for options that fit the
    'Safe Yield' criteria (Low Delta, ~30 days out).
    """
    target_delta_min = target_delta_min or MIN_DELTA
    target_delta_max = target_delta_max or MAX_DELTA

    ticker = yf.Ticker(symbol)
    current_price = ticker.fast_info['last_price']

    expirations = ticker.options
    target_date = expirations[min(2, len(expirations) - 1)]

    chain = ticker.option_chain(target_date)

    days_to_expiry = (datetime.strptime(target_date, "%Y-%m-%d") - datetime.now()).days
    T = max(days_to_expiry, 1) / 365.0

    results = []
    for _, row in chain.calls.iterrows():
        delta = calculate_delta(current_price, row['strike'], T, RISK_FREE_RATE, row['impliedVolatility'])

        if target_delta_min <= delta <= target_delta_max:
            results.append({
                "Ticker": symbol,
                "Price": f"${current_price:.2f}",
                "Strike": f"${row['strike']:.2f}",
                "Delta": f"{delta:.2f}",
                "Premium": f"${row['lastPrice']:.2f}",
                "Expiry": target_date
            })
            break

    return results
