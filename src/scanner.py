import yfinance as yf
from datetime import datetime
from .calculators import calculate_delta

def find_safe_options(symbol, target_delta_min=0.15, target_delta_max=0.20):
    """
    Connects to Yahoo Finance and filters for options that fit the 
    'Safe Yield' criteria (Low Delta, ~30 days out).
    """
    ticker = yf.Ticker(symbol)
    
    # fast_info is used for the absolute latest price on the NUC
    current_price = ticker.fast_info['last_price']
    
    # Select expiration: Index [2] usually targets 3-5 weeks out.
    # This captures the 'sweet spot' of Theta (time decay).
    expirations = ticker.options
    target_date = expirations[min(2, len(expirations)-1)] 
    
    # Fetch the full call/put data for that date
    chain = ticker.option_chain(target_date)
    
    # Convert dates to a 'Time' value for the math model (T)
    days_to_expiry = (datetime.strptime(target_date, "%Y-%m-%d") - datetime.now()).days
    T = max(days_to_expiry, 1) / 365.0
    
    results = []
    # Loop through all available CALL options
    for _, row in chain.calls.iterrows():
        # Calculate Delta using our Math Lab tool
        # Using 0.04 as a standard 2026 interest rate
        delta = calculate_delta(current_price, row['strike'], T, 0.04, row['impliedVolatility'])
        
        # Filter: Only keep strikes that fit your 'Safe Zone'
        if target_delta_min <= delta <= target_delta_max:
            results.append({
                "Ticker": symbol,
                "Price": f"${current_price:.2f}",
                "Strike": f"${row['strike']:.2f}",
                "Delta": f"{delta:.2f}",
                "Premium": f"${row['lastPrice']:.2f}",
                "Expiry": target_date
            })
            # Once we find the best match for this stock, move to the next stock
            break 
            
    return results