from datetime import datetime
import pandas as pd
from tabulate import tabulate
from .scanner import find_safe_options

def run_daily_report():
    """
    The main execution loop. It aggregates data for all your holdings
    and presents it in the dual-table format.
    """
    # Your core long-term holdings
    my_stocks = ["AAPL", "TSLA", "SCHD", "MSFT"]
    all_opportunities = []
    
    print(f"--- SCANNING MARKET FOR SAFE YIELD ---")
    
    for stock in my_stocks:
        # Run the scout for each stock
        opps = find_safe_options(stock)
        if opps:
            all_opportunities.extend(opps)
            
    # --- TABLE 1: DETAILED DELTA REPORT ---
    df = pd.DataFrame(all_opportunities)
    print(f"\nDETAILED TRADES (Target Delta: 0.15 - 0.20)")
    print(tabulate(df, headers='keys', tablefmt='grid'))

    # --- TABLE 2: MONTHLY SUMMARY ---
    # Convert premium strings back to numbers for the sum
    total_premium = sum([float(x['Premium'].replace('$', '')) for x in all_opportunities])
    summary = [[
        datetime.now().strftime("%B %Y"), 
        f"${total_premium:.2f}", 
        "STRATEGY: HOLDING & COLLECTING"
    ]]
    
    print(f"\nMONTHLY YIELD SUMMARY")
    print(tabulate(summary, headers=["Month", "Total Est. Premium", "Status"], tablefmt='grid'))

if __name__ == "__main__":
    run_daily_report()