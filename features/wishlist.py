from telegram import Update
from telegram.ext import ContextTypes
from tinydb import TinyDB, Query

# Load or create wishlist database
wishlist_db = TinyDB("wishlist.json")
Wishlist = Query()

# Add item to wishlist by UPC
async def add_to_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /addtowishlist <UPC>")
        return

    upc = context.args[0]
    user_id = str(update.effective_user.id)

    # Check if item already exists
    exists = wishlist_db.search((Wishlist.user_id == user_id) & (Wishlist.upc == upc))
    if exists:
        await update.message.reply_text("Item already in your wishlist.")
        return

    wishlist_db.insert({"user_id": user_id, "upc": upc})
    await update.message.reply_text(f"✅ Added UPC {upc} to your wishlist.")

# View user's wishlist
async def view_wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    items = wishlist_db.search(Wishlist.user_id == user_id)

    if not items:
        await update.message.reply_text("Your wishlist is empty.")
        return

    upcs = [item["upc"] for item in items]
    result = "\n".join(upcs)
    await update.message.reply_text(f"📝 Your wishlist:\n{result}")
    from features.clearance import get_clearance_items, calc_discount

async def check_and_notify_wishlist(bot, user_id: str, chat_id: int):
    items = wishlist_db.search(Wishlist.user_id == user_id)
    if not items:
        return

    upcs = [item["upc"] for item in items]
    clearance_items = get_clearance_items()

    found_items = []
    for item in clearance_items:
        if "upc" in item and item["upc"] in upcs:
            discount = calc_discount(item)
            if discount >= 40:
                emoji = "🔥" if discount >= 60 else ""
                found_items.append(f"{emoji}{item['name']}\nOriginal: ${item['original_price']} → Now: ${item['price']} ({discount}% off)")

    if found_items:
        message = "🎯 Items from your wishlist are now discounted:\n\n" + "\n\n".join(found_items)
        await bot.send_message(chat_id=chat_id, text=message)
