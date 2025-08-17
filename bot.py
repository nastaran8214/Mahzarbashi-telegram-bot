import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Config from Environment ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

# OpenAI (legacy SDK for simplicity)
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "تو یک مشاور حقوقی حرفه‌ای و دقیق برای کاربران فارسی‌زبان هستی. "
    "پاسخ‌ها باید روشن، مودبانه و بر پایه قوانین ایران باشد (اگر کاربر کشور دیگری گفت، همان کشور را ملاک بگیر). "
    "اگر اطلاعات کافی نداری، با سوالات روشن، مورد را مشخص کن. "
    "اخطار عدم جایگزینی با وکیل را مختصر در انتهای پاسخ اضافه کن."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات مشاور حقوقی محضرباشی هستم. "
        "سوال حقوقی‌تون رو بپرسید تا راهنمایی‌تون کنم."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = (update.message.text or "").strip()
    if not user_text:
        return

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            max_tokens=500,
            temperature=0.4,
        )
        answer = completion["choices"][0]["message"]["content"].strip()
    except Exception as e:
        answer = "خطایی رخ داد. لطفاً دوباره تلاش کنید."
        print("OpenAI error:", e)

    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running with long polling ...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, stop_signals=None)

if name == "__main__":
    main()
