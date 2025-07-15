from telegram import Update
from telegram.ext import ContextTypes

CATEGORIES = {
    "Baby": ["Pampers", "Wipes", "Formula"],
    "Beauty": ["Mascara", "Lip Gloss", "Foundation"],
    "Health": ["Vitamins", "Pain Relief", "Cough Syrup"],
    "Food": ["Cereal", "Snacks", "Drinks"],
    "Home": ["Cleaning Supplies", "Furniture", "Decor"],
    "Electronics": ["TV", "Headphones", "Phones"],
    "Automotive": ["Motor Oil", "Tires", "Car Battery"]
}

async def list_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛍️ Available Categories:\n" + "\n".join(f"• {cat}" for cat in CATEGORIES.keys())
    text += "\n\nUse /category <name> to explore."
    await update.message.reply_text(text)

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /category <name>\nExample: /category Electronics")
        return
    
    category = context.args[0].capitalize()
    items = CATEGORIES.get(category)
    
    if items:
        item_list = "\n".join(f"• {item}" for item in items)
        await update.message.reply_text(f"🧾 Sample items in {category}:\n{item_list}")
    else:
        await update.message.reply_text(f"❌ Unknown category: {category}")
