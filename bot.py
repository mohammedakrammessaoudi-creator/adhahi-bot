import requests
import time

TOKEN = "8627534186:AAHgbxBR8N8WXZeaeIXC7yL05OSlXs6gnKk"
CHAT_ID = "6772308497"
URL = "https://adhahi.dz/register"

def check_site():
    try:
        r = requests.get(URL, timeout=10)
        if r.status_code == 200 and "register" in r.url:
            return True
    except:
        pass
    return False

def send_message(text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": text})

print("Bot started...")
notified = False

while True:
    if check_site() and not notified:
        send_message("🚨 موقع الأضاحي فتح التسجيل! سجل دروك: https://adhahi.dz/register")
        notified = True
        print("Notification sent!")
    else:
        print("Site still closed...")
        notified = False
    time.sleep(300)
