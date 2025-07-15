from telegram import Update
from telegram.ext import ContextTypes

categories = {
    "Electronics": ["TV", "Laptop", "Headphones"],
    "Home": ["Furniture", "Vacuum", "Curtains"],
    "Beauty": ["Shampoo", "Lotion", "Makeup"],
    "Baby": ["Diapers", "Wipes", "Formula"],
    "Health": ["Vitamins", "Pain Relief", "Thermometer"],
    "Food": ["Snacks", "Cereal", "Frozen Meals"],
}

async def list_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📂 Available Categories:\n" + "\n".join([f"• {name}" for name in categories])
    await update.message.reply_text(text)

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        name = " ".join(context.args)
        if name in categories:
            items = "\n".join([f"- {item}" for item in categories[name]])
            await update.message.reply_text(f"📦 {name} items:\n{items}")
        else:
            await update.message.reply_text("❌ Category not found. Try /categories to see all options.")
    except:
        await update.message.reply_text("⚠️ Usage: /category <Category Name>")
