import telebot
import requests
from bs4 import BeautifulSoup
import time

# --- الإعدادات ---
TOKEN = "ضع_هنا_التوكن_تاعك" # استبدل هذه الجملة بالتوكن اللي عطاهولك BotFather
URL = "https://adhahi.dz/register" # رابط موقع الأضاحي (هنا البوت يعرف وين يروح)
CHAT_ID = "ضع_هنا_الآيدي_تاعك" # الآيدي تاعك باش يبعثلك ميساج

bot = telebot.TeleBot(TOKEN)

def check_batna():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        # هنا البوت يحوس على كلمة "باتنة" في الصفحة
        if "باتنة" in soup.text: 
            return True
        return False
    except:
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلا برو! أنا بوت الأضاحي 🐑\nراني نعس في موقع adhahi.dz، غير تفتح باتنة نبعثلك!")

@bot.message_handler(commands=['status'])
def check_status(message):
    if check_batna():
        bot.reply_to(message, "✅ باتنة راهي مفتوحة! أزرب سجل!")
    else:
        bot.reply_to(message, "❌ باتنة مازالها مغلقة، اصبر شوية.")

# حلقة المراقبة (تشتغل في الخلفية)
def monitor():
    while True:
        if check_batna():
            bot.send_message(CHAT_ID, "🚨 برو!! باتنة فتحت الآن! ادخل سجل فوراً: " + URL)
            time.sleep(60) # يستنى دقيقة باش ما يبقاش يبعث كل ثانية
        time.sleep(10) # يشيك كل 10 ثواني

# لتشغيل المراقبة مع البوت في غليتش
import threading
threading.Thread(target=monitor, daemon=True).start()

bot.infinity_polling()
