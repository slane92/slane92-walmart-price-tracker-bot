# 🛒 Walmart Price Tracker Bot

A Telegram bot that checks Walmart inventory prices by UPC and ZIP code, sorts stores by distance, and can send alerts (via Telegram and SMS).

---

## ✅ Commands

- `/start` – Show welcome message
- `/check <UPC> <ZIP>` – Find Walmart store prices near ZIP
- `/alert <UPC> <ZIP> <price>` – (Future) Set price drop alert
- `/browse` – (Future) Browse categories

---

## 🛠 How to Deploy on Render

1. Add these environment variables:
   - `TELEGRAM_BOT_TOKEN` → from BotFather
   - `DEFAULT_ZIPS` → `92131,92126`

2. Requirements install automatically via `requirements.txt`

3. App runs via `Procfile`:  
