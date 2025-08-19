import os
import openai
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters

# گرفتن کلیدها از Environment
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = Flask(__name__)
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# دستور /start
def start(update, context):
    update.message.reply_text("سلام! من ربات مشاور حقوقی محضرباشی هستم. سوال حقوقی‌تون رو بپرسید.")

# پردازش پیام‌ها
def handle_message(update, context):
    user_text = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "تو یک مشاور حقوقی حرفه‌ای هستی و جواب‌های دقیق و کامل می‌دهی."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=400
        )
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        print("Error:", e)
        answer = "مشکلی در دریافت پاسخ پیش آمد، دوباره تلاش کنید."
    update.message.reply_text(answer)

# تنظیم Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Mahzarbashi Assistant Bot is running!"
