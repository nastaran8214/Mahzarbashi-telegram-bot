# Mahzarbashi Telegram Bot (Polling)

ربات مشاور حقوقی محضرباشی با Long Polling (بدون وبهوک). اجرای دائم روی Render به‌صورت Background Worker.

## 1) متغیرهای محیطی
در Render در بخش Environment:
- TELEGRAM_TOKEN = توکن ربات تلگرام شما
- OPENAI_API_KEY = کلید OpenAI

## 2) دیپلوی روی Render (ساده‌ترین حالت)
1. روی Render: New → Background Worker
2. ریپازیتوری GitHub: Mahzarbashi-telegram-bot
3. Build Command: pip install -r requirements.txt
4. Start Command: python bot.py
5. Region: Europe (Frankfurt)
6. Create Worker

> چون Long Polling است، نیازی به Webhook نیست.
