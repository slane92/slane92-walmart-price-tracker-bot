from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from walmart_api import get_walmart_prices_near_zip
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_ZIPS = os.getenv("DEFAULT_ZIPS", "92131").split(",")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Walmart Price Tracker Bot!\nType /check <UPC> <ZIP> to check prices nearby.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❗ Usage: /check <UPC> <ZIP>\nExample: /check 884392951955 92131")
        return
    upc = context.args[0]
    zip_code = context.args[1]
    results = get_walmart_prices_near_zip(upc, zip_code)
    if not results:
        await update.message.reply_text("❌ No price data found.")
        return

    response = f"🛒 Prices for UPC {upc} near {zip_code}:\n\n"
    for r in results:
        response += f"{r['store']} – {r['distance']} mi – ${r['price']:.2f}\n"
    await update.message.reply_text(response)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.run_polling()
