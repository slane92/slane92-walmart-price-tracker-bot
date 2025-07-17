# wishlist.py
from telegram import Update
from telegram.ext import ContextTypes
from db import db  # Assumes TinyDB is set up

def get_user_wishlist(user_id):
    user_data = db.get(doc_id=user_id)
    return user_data.get("wishlist", []) if user_data else []

def add_to_wishlist(user_id, upc):
    user_data = db.get(doc_id=user_id)
    if not user_data:
        db.insert({"wishlist": [upc]}, doc_id=user_id)
    else:
        wishlist = user_data.get("wishlist", [])
        if upc not in wishlist:
            wishlist.append(upc)
            db.update({"wishlist": wishlist}, doc_ids=[user_id])

async def addtowishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Please provide a UPC to add to your wishlist.")
        return
    upc = context.args[0]
    add_to_wishlist(user_id, upc)
    await update.message.reply_text(f"✅ UPC {upc} added to your wishlist!")

async def wishlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wishlist_items = get_user_wishlist(user_id)
    if not wishlist_items:
        await update.message.reply_text("Your wishlist is currently empty.")
    else:
        await update.message.reply_text("📝 Your Wishlist UPCs:\n" + "\n".join(wishlist_items))
