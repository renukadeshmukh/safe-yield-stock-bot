from datetime import datetime
import pandas as pd
from tabulate import tabulate
from .strategy.scanner import find_safe_options
from .config import MY_STOCKS


def run_daily_report():
    """
    The main execution loop. Aggregates data for all holdings
    and presents it in the dual-table format.
    """
    all_opportunities = []

    print("--- SCANNING MARKET FOR SAFE YIELD ---")

    for stock in MY_STOCKS:
        opps = find_safe_options(stock)
        if opps:
            all_opportunities.extend(opps)

    df = pd.DataFrame(all_opportunities)
    print(f"\nDETAILED TRADES (Target Delta: 0.15 - 0.20)")
    print(tabulate(df, headers='keys', tablefmt='grid'))

    total_premium = sum(float(x['Premium'].replace('$', '')) for x in all_opportunities)
    summary = [[
        datetime.now().strftime("%B %Y"),
        f"${total_premium:.2f}",
        "STRATEGY: HOLDING & COLLECTING"
    ]]

    print(f"\nMONTHLY YIELD SUMMARY")
    print(tabulate(summary, headers=["Month", "Total Est. Premium", "Status"], tablefmt='grid'))


if __name__ == "__main__":
    run_daily_report()
