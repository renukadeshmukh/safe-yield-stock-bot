from unittest.mock import patch, MagicMock
from src.integrations.nlp_parser import parse_trade


def _mock_response(json_str):
    resp = MagicMock()
    resp.text = json_str
    return resp


@patch("src.integrations.nlp_parser._model.generate_content")
def test_parse_basic_covered_call(mock_gen):
    mock_gen.return_value = _mock_response(
        '{"ticker":"AAPL","action":"SELL_TO_OPEN","quantity":1,"strike":230.0,"expiry":"2026-04-18","premium":3.45}'
    )
    result = parse_trade("Sold 1 AAPL Apr 18 230 Call @ 3.45")
    assert result["ticker"] == "AAPL"
    assert result["action"] == "SELL_TO_OPEN"
    assert result["strike"] == 230.0
    assert result["premium"] == 3.45


@patch("src.integrations.nlp_parser._model.generate_content")
def test_parse_handles_markdown_fences(mock_gen):
    mock_gen.return_value = _mock_response(
        '```json\n{"ticker":"TSLA","action":"SELL_TO_OPEN","quantity":2,"strike":400.0,"expiry":"2026-05-16","premium":8.10}\n```'
    )
    result = parse_trade("Sold 2 TSLA May 16 400 Call @ 8.10")
    assert result["ticker"] == "TSLA"
    assert result["quantity"] == 2


@patch("src.integrations.nlp_parser._model.generate_content")
def test_parse_returns_none_on_garbage(mock_gen):
    mock_gen.return_value = _mock_response("I don't understand that input")
    assert parse_trade("random garbage") is None
