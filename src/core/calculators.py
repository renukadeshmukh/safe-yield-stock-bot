import numpy as np
from scipy.stats import norm

def calculate_delta(S, K, T, r, sigma):
    """
    Calculates the 'Delta' of a call option using the Black-Scholes model.
    
    Parameters:
    S: Current Stock Price
    K: Strike Price of the Option
    T: Time to Expiration (in years, e.g., 30 days = 30/365)
    r: Risk-free interest rate (current 10-year Treasury yield is a good proxy)
    sigma: Implied Volatility (The market's expectation of future movement)
    
    Strategy Note: Delta represents the probability that the option will expire 
    In-The-Money (ITM). A 0.15 Delta means ~15% chance of assignment.
    """
    # Safety check: If time or volatility is 0, we can't calculate a valid Delta
    if T <= 0 or sigma <= 0: 
        return 0
        
    # d1 is a core component of the Black-Scholes formula representing 
    # the probability-weighted distance to the strike price.
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    # norm.cdf converts d1 into a cumulative probability (0 to 1)
    return norm.cdf(d1)