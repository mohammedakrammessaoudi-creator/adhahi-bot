import requests
import time
from bs4 import BeautifulSoup

TOKEN = "8627534186:AAHgbxBR8N8WXZeaeIXC7yL05OSlXs6gnKk"
CHAT_ID = "6772308497"
URL = "https://adhahi.dz/register"

def check_batna():
    try:
        r = requests.get(URL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text()
        if "باتنة" in text and "غير متوفر" not in text.split("باتنة")[1][:50]:
            return True
    except:
        pass
    return False

def send_message(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": text})

print("Bot started - watching Batna...")
notified = False

while True:
    if check_batna() and not notified:
        send_message("🚨 باتنة فتحت التسجيل! سجل دروك: https://adhahi.dz/register")
        notified = True
        print("Notification sent!")
    else:
        print("Batna still closed...")
        notified = False
    time.sleep(300)
