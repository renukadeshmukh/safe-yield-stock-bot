from datetime import date
from calendar import monthrange


def prorate_premium(total_premium: float, start_date: date, end_date: date) -> dict[str, float]:
    """
    Pro-rate a premium across months based on days active.

    Daily Rate = Total Premium / Total Days in Trade
    Month Allocation = Daily Rate × Days Active in Month

    Returns dict of "YYYY-MM" -> allocated amount.
    """
    total_days = (end_date - start_date).days
    if total_days <= 0:
        return {}

    daily_rate = total_premium / total_days
    allocations = {}
    current = start_date

    while current < end_date:
        month_key = current.strftime("%Y-%m")
        month_end = date(current.year, current.month, monthrange(current.year, current.month)[1])
        period_end = min(month_end, end_date)
        days_in_period = (period_end - current).days + (1 if period_end == end_date else 0)
        # Don't count the end_date day itself unless it's the final period
        if period_end < end_date:
            days_in_period = (period_end - current).days + 1
        else:
            days_in_period = (end_date - current).days

        allocations[month_key] = round(daily_rate * days_in_period, 2)

        # Move to first of next month
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)

    return allocations
