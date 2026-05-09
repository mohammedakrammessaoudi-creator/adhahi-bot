import requests
import time
import threading
from bs4 import BeautifulSoup

TOKEN = "8627534186:AAHgbxBR8N8WXZeaeIXC7yL05OSlXs6gnKk"
CHAT_ID = "6772308497"
URL = "https://adhahi.dz/register"

batna_open = False

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

def send_message(chat_id, text):
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                 params={"chat_id": chat_id, "text": text})

def get_updates(offset=None):
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", params=params, timeout=35)
        return r.json()
    except:
        return {}

def listen_messages():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            if text == "/status":
                if batna_open:
                    send_message(chat_id, "🟢 باتنة فتحت التسجيل!")
                else:
                    send_message(chat_id, "🔴 باتنة مزال مغلق")

def monitor():
    global batna_open
    notified = False
    while True:
        batna_open = check_batna()
        if batna_open and not notified:
            send_message(CHAT_ID, "🚨 باتنة فتحت التسجيل! سجل دروك: https://adhahi.dz/register")
            notified = True
        elif not batna_open:
            notified = False
        time.sleep(10)

print("Bot started - watching Batna...")
t1 = threading.Thread(target=listen_messages)
t2 = threading.Thread(target=monitor)
t1.start()
t2.start()
