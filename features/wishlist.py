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
