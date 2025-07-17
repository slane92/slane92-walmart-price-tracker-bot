# Paste starting here
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import os
from tinydb import TinyDB, Query

from features.clearance import run_clearance_scan, format_clearance_message
from features.wishlist import add_wishlist, remove_wishlist, show_wishlist
from features.admin import adminpanel, settings, logme, addtester, removetester
from features.categories import list_categories, show_category
from features.search import search_product
from features.storefinder import find_stores

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
db = TinyDB("db.json")
User = Query()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /setzip <ZIP> to begin.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Core handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setzip", lambda u,c: await_setzip(u,c)))  # ensure setzip defined
app.add_handler(CommandHandler("clearance", clearance_handler))

# Wishlist
app.add_handler(CommandHandler("addtowishlist", add_wishlist))
app.add_handler(CommandHandler("removewishlist", remove_wishlist))
app.add_handler(CommandHandler("wishlist", show_wishlist))

# Markdown scan
app.add_handler(CommandHandler("markdowns", markdowns_handler))

# Search, categories, storefinder
app.add_handler(CommandHandler("search", search_product))
app.add_handler(CommandHandler("categories", list_categories))
app.add_handler(CommandHandler("category", show_category))
app.add_handler(CommandHandler("stores", find_stores))

# Admin
app.add_handler(CommandHandler("adminpanel", adminpanel))
app.add_handler(CommandHandler("settings", settings))
app.add_handler(CommandHandler("logme", logme))
app.add_handler(CommandHandler("addtester", addtester))
app.add_handler(CommandHandler("removetester", removetester))

app.add_handler(CallbackQueryHandler(handle_button_click))

print("Bot is running!")
app.run_polling()
# End of main.py
