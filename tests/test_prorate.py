from datetime import date
from src.core.prorate import prorate_premium


def test_equal_split_across_two_months():
    """$300 over 30 days (15 days each month) = $150/$150."""
    result = prorate_premium(300.0, date(2026, 3, 16), date(2026, 4, 15))
    assert result["2026-03"] == 160.0  # 16 days (Mar 16-31)
    assert result["2026-04"] == 140.0  # 14 days (Apr 1-14, not including Apr 15 end)
    assert abs(sum(result.values()) - 300.0) < 0.01


def test_single_month():
    """Entire trade within one month."""
    result = prorate_premium(100.0, date(2026, 6, 1), date(2026, 6, 30))
    assert "2026-06" in result
    assert len(result) == 1
    assert abs(result["2026-06"] - 100.0) < 0.01


def test_three_month_span():
    """Trade spanning 3 months."""
    result = prorate_premium(900.0, date(2026, 1, 15), date(2026, 4, 15))
    assert len(result) == 4  # Jan, Feb, Mar, Apr
    assert abs(sum(result.values()) - 900.0) < 0.01


def test_zero_days_returns_empty():
    result = prorate_premium(100.0, date(2026, 1, 1), date(2026, 1, 1))
    assert result == {}
