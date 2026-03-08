import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ..config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


async def send_message(app: Application, text: str, chat_id: str = None):
    """Send a message to the configured chat."""
    chat_id = chat_id or TELEGRAM_CHAT_ID
    await app.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ *Safe Yield Bot Active*\n\n"
        "Commands:\n"
        "/scan — Run option scanner\n"
        "/status — Show active positions\n"
        "/help — Show this message\n\n"
        "Or paste raw brokerage text to log a trade.",
        parse_mode="Markdown"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, context)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle free-text messages — route to NLP parser."""
    raw_text = update.message.text
    # Lazy import to avoid circular deps
    from ..integrations.nlp_parser import parse_trade

    await update.message.reply_text("🔍 Parsing your trade...")
    result = parse_trade(raw_text)

    if result:
        msg = (
            f"✅ *Trade Parsed*\n"
            f"Ticker: `{result.get('ticker')}`\n"
            f"Action: `{result.get('action')}`\n"
            f"Qty: `{result.get('quantity')}`\n"
            f"Strike: `${result.get('strike')}`\n"
            f"Expiry: `{result.get('expiry')}`\n"
            f"Premium: `${result.get('premium')}`"
        )
    else:
        msg = "❌ Could not parse trade. Please try again with clearer text."

    await update.message.reply_text(msg, parse_mode="Markdown")


def create_bot() -> Application:
    """Build and return the Telegram bot application."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    return app


def run_bot():
    """Start the bot in long-polling mode."""
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting Telegram bot...")
    app = create_bot()
    app.run_polling()
