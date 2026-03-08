from unittest.mock import patch, MagicMock
from src.integrations.healthcheck import ping_health, ping_fail


@patch("src.integrations.healthcheck.HEALTHCHECK_URL", "https://hc-ping.com/test-uuid")
@patch("src.integrations.healthcheck.requests.get")
def test_ping_health_calls_url(mock_get):
    ping_health()
    mock_get.assert_called_once_with("https://hc-ping.com/test-uuid", timeout=5)


@patch("src.integrations.healthcheck.HEALTHCHECK_URL", "https://hc-ping.com/test-uuid")
@patch("src.integrations.healthcheck.requests.get")
def test_ping_fail_calls_fail_url(mock_get):
    ping_fail("something broke")
    mock_get.assert_called_once_with("https://hc-ping.com/test-uuid/fail", timeout=5)


@patch("src.integrations.healthcheck.HEALTHCHECK_URL", None)
@patch("src.integrations.healthcheck.requests.get")
def test_ping_skips_when_no_url(mock_get):
    ping_health()
    mock_get.assert_not_called()
