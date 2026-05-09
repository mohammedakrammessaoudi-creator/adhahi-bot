import requests
import time
import threading
import json
import os
from bs4 import BeautifulSoup

TOKEN = "8627534186:AAHgbxBR8N8WXZeaeIXC7yL05OSlXs6gnKk"
URL = "https://adhahi.dz/register"
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

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

def broadcast(text):
    for uid in users:
        send_message(uid, text)

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
    global users
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            if not chat_id:
                continue
            if text == "/start":
                if chat_id not in users:
                    users.append(chat_id)
                    save_users(users)
                send_message(chat_id, "أهلاً! ✅ تسجلت في التنبيهات\nراح يجيك إشعار فوري كي تفتح باتنة 🚨")
            elif text == "/status":
                if check_batna():
                    send_message(chat_id, "🟢 باتنة فتحت التسجيل!")
                else:
                    send_message(chat_id, "🔴 باتنة مزال مغلق")
            else:
                send_message(chat_id, "أهلاً! 👋\nابعث /start باش تتسجل في التنبيهات\nابعث /status باش تشوف حالة باتنة")

def monitor():
    notified = False
    while True:
        if check_batna() and not notified:
            broadcast("🚨 باتنة فتحت التسجيل! سجل دروك: https://adhahi.dz/register")
            notified = True
        elif not check_batna():
            notified = False
        time.sleep(10)

print("Bot started - watching Batna...")
t1 = threading.Thread(target=listen_messages)
t2 = threading.Thread(target=monitor)
t1.start()
t2.start()
