import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# إعدادات البوت
TOKEN = os.getenv("TELEGRAM_TOKEN", "ضع_هنا_التوكن_تاعك")
URL_CHECK = "https://adhahi.dz/status" # الرابط اللي يراقب حالة باتنة

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا برو! أنا بوت الأضاحي، راني نعس في باتنة، غير تفتح نبعثلك!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # هنا البوت يروح يشوف السيت واش قال على باتنة
    response = requests.get(URL_CHECK).json()
    state = response.get("batna", "غير معروف")
    await update.message.reply_text(f"حالة باتنة حالياً هي: {state}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()
