import telebot
import requests
from bs4 import BeautifulSoup
import time

# --- الإعدادات (الكونفيغ) ---
TOKEN = "123456789:ABCdefGHIjkl"  # حط هنا التوكن تاعك اللي عطاهولك BotFather
URL = "https://adhahi.dz/register" # هذا هو الرابط اللي يخلي البوت يعرف السيت
MY_CHAT_ID = "12345678"            # حط هنا الـ ID تاعك باش يبعثلك الإشعار

bot = telebot.TeleBot(TOKEN)

def check_batna():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # هنا البوت يحوس على كلمة "باتنة" في الجدول تاع السيت
        rows = soup.find_all('tr')
        for row in rows:
            if "باتنة" in row.text:
                if "مفتوحة" in row.text:
                    return True # باتنة فتحت!
                else:
                    return False # باتنة مازالها مغلقة
    except:
        return None # صرا مشكل في الكونيكسيون

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلا برو! راني نراقب في موقع الأضاحي على جال باتنة 🐑")

@bot.message_handler(commands=['status'])
def send_status(message):
    if check_batna():
        bot.reply_to(message, "✅ باتنة راهي مفتوحة! أزرب سجل!")
    else:
        bot.reply_to(message, "❌ باتنة مازالت مغلقة.. اصبر شوية.")

# حلقة المراقبة (تخدم في الخلفية)
def monitor():
    while True:
        if check_batna():
            bot.send_message(MY_CHAT_ID, "🚨 برووو! باتنة فتحت! أدخل سجل فوراً: " + URL)
            # كي تفتح باتنة، نحبسوا المراقبة مؤقتاً أو نخلوها كل ساعة
            time.sleep(3600)
        time.sleep(10) # يشيك كل 10 ثواني

# باش يخدم المونيتور مع البوت في Glitch
import threading
threading.Thread(target=monitor).start()

bot.polling()
