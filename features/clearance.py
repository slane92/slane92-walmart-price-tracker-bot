from telegram import Update
from telegram.ext import ContextTypes
from tinydb import TinyDB, Query

# Load database
db = TinyDB("db.json")
User = Query()

# Mock data source – replace this with real logic if pulling from an API
def get_clearance_items():
    return [
        {"name": "Toy Car", "price": 9.99, "original_price": 24.99},
        {"name": "Smart Light", "price": 19.99, "original_price": 39.99},
        {"name": "Air Fryer", "price": 49.99, "original_price": 129.99},
        {"name": "Shampoo", "price": 6.99, "original_price": 14.99},
        {"name": "Vacuum", "price": 89.99, "original_price": 199.99},
    ]

# Utility
def calc_discount(item):
    original = item["original_price"]
    current = item["price"]
    discount = round(100 - ((current / original) * 100))
    return discount

def format_item(item):
    discount = calc_discount(item)
    emoji = "🔥" if discount >= 60 else ""
    return f"{emoji}{item['name']}\nOriginal: ${item['original_price']} → Now: ${item['price']} ({discount}% off)"

# Main markdown handler
async def run_clearance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = get_clearance_items()
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No clearance items found.")

# % threshold handlers
async def markdowns_40(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if calc_discount(i) >= 40]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items 40% off or more.")

async def markdowns_50(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if calc_discount(i) >= 50]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items 50% off or more.")

async def markdowns_60(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if calc_discount(i) >= 60]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items 60% off or more.🔥")

# Price group handlers
async def under10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if i["price"] <= 10]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items $10 or less.")

async def under20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if i["price"] <= 20]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items $20 or less.")

async def under40(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = [i for i in get_clearance_items() if i["price"] <= 40]
    result = "\n\n".join([format_item(i) for i in items])
    await update.message.reply_text(result or "No items $40 or less.")
