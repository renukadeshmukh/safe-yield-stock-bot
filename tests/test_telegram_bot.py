from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from src.integrations.telegram_bot import cmd_start, handle_text


@pytest.mark.asyncio
async def test_start_command_replies():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    await cmd_start(update, MagicMock())
    update.message.reply_text.assert_called_once()
    call_text = update.message.reply_text.call_args[0][0]
    assert "Safe Yield Bot Active" in call_text


@pytest.mark.asyncio
@patch("src.integrations.nlp_parser._model.generate_content")
async def test_handle_text_parses_trade(mock_gen):
    mock_gen.return_value = MagicMock(
        text='{"ticker":"AAPL","action":"SELL_TO_OPEN","quantity":1,"strike":230.0,"expiry":"2026-04-18","premium":3.45}'
    )
    update = MagicMock()
    update.message.text = "Sold 1 AAPL Apr 18 230 Call @ 3.45"
    update.message.reply_text = AsyncMock()

    await handle_text(update, MagicMock())

    # Should have two replies: "Parsing..." and the result
    assert update.message.reply_text.call_count == 2
    result_text = update.message.reply_text.call_args_list[1][0][0]
    assert "AAPL" in result_text
    assert "Trade Parsed" in result_text


@pytest.mark.asyncio
@patch("src.integrations.nlp_parser._model.generate_content")
async def test_handle_text_reports_parse_failure(mock_gen):
    mock_gen.return_value = MagicMock(text="garbage")
    update = MagicMock()
    update.message.text = "random nonsense"
    update.message.reply_text = AsyncMock()

    await handle_text(update, MagicMock())

    result_text = update.message.reply_text.call_args_list[1][0][0]
    assert "Could not parse" in result_text
