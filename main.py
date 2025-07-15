 from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tinydb import TinyDB, Query

import os
from walmart_api import search_walmart_item

# Load bot token from environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize TinyDB
db = TinyDB("db.json")
User = Query()

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Walmart Price Bot!\nUse /setzip <ZIP> to begin.")

# /setzip command
async def set_zip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        zip_code = context.args[0]
        db.upsert({"id": update.effective_user.id, "zip": zip_code}, User.id == update.effective_user.id)
        await update.message.reply_text(f"✅ ZIP code set to {zip_code}")
    except IndexError:
        await update.message.reply_text("⚠️ Please provide a ZIP code: /setzip 92131")

# /getzip command
async def get_zip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = db.get(User.id == update.effective_user.id)
    if user_data and "zip" in user_data:
        await update.message.reply_text(f"📍 Your ZIP code is: {user_data['zip']}")
    else:
        await update.message.reply_text("⚠️ You haven't set a ZIP code yet. Use /setzip <ZIP>.")

# /addtolist UPC
async def add_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        upc = context.args[0]
        user_data = db.get(User.id == update.effective_user.id)
        if not user_data:
            db.insert({"id": update.effective_user.id, "zip": "", "list": [upc]})
        else:
            current_list = user_data.get("list", [])
            if upc not in current_list:
                current_list.append(upc)
                db.update({"list": current_list}, User.id == update.effective_user.id)
        await update.message.reply_text(f"✅ Added UPC {upc} to your shopping list.")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /addtolist <UPC>")

# /list command
async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = db.get(User.id == update.effective_user.id)
    if user_data and "list" in user_data:
        upcs = user_data["list"]
        if upcs:
            msg = "🛒 Your shopping list:\n" + "\n".join([f"- {upc}" for upc in upcs])
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("🛒 Your shopping list is empty.")
    else:
        await update.message.reply_text("🛒 You have no saved shopping list yet.")

# /price UPC
async def check_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        upc = context.args[0]
        price = search_walmart_item(upc)  # You need to define this in walmart_api.py
        await update.message.reply_text(f"💲Current price for UPC {upc}: {price}")
    except IndexError:
        await update.message.reply_text("⚠️ Usage: /price <UPC>")

# Bot startup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setzip", set_zip))
    app.add_handler(CommandHandler("getzip", get_zip))
    app.add_handler(CommandHandler("addtolist", add_to_list))
    app.add_handler(CommandHandler("list", show_list))
    app.add_handler(CommandHandler("price", check_price))

    print("✅ Bot is running...")

    app.run_polling()   
