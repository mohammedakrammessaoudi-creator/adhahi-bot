import requests
import time
import threading
from bs4 import BeautifulSoup

TOKEN = "8627534186:AAHgbxBR8N8WXZeaeIXC7yL05OSlXs6gnKk"
URL = "https://adhahi.dz/register"

users = []

WILAYAS = [
    "أدرار", "الشلف", "الأغواط", "أم البواقي", "باتنة", "بجاية",
    "بسكرة", "بشار", "البليدة", "البويرة", "تمنراست", "تبسة",
    "تلمسان", "تيارت", "تيزي وزو", "الجزائر", "الجلفة", "جيجل",
    "سطيف", "سعيدة", "سكيكدة", "سيدي بلعباس", "عنابة", "قالمة",
    "قسنطينة", "المدية", "مستغانم", "المسيلة", "معسكر", "ورقلة",
    "وهران", "البيض", "إليزي", "برج بوعريريج", "بومرداس", "الطارف",
    "تندوف", "تيسمسيلت", "الوادي", "خنشلة", "سوق أهراس", "تيبازة",
    "ميلة", "عين الدفلى", "النعامة", "عين تموشنت", "غرداية", "غليزان",
    "تيميمون", "برج باجي مختار", "أولاد جلال", "بني عباس", "عين صالح",
    "عين قزام", "توقرت", "جانت", "المغير", "المنيعة"
]

def check_wilaya(wilaya):
    try:
        r = requests.get(URL, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text()
        if wilaya in text:
            idx = text.split(wilaya)[1][:80]
            if "غير متوفر" not in idx:
                return True
    except:
        pass
    return False

def get_open_wilayas():
    open_list = []
    for w in WILAYAS:
        if check_wilaya(w):
            open_list.append(w)
    return open_list

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
        r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates",
                        params=params, timeout=35)
        return r.json()
    except:
        return {}

def smart_reply(text, chat_id):
    text = text.strip().lower()

    if "/start" in text:
        if chat_id not in users:
            users.append(chat_id)
        send_message(chat_id, "أهلاً برو! 👋\nأنا بوت الأضاحي — راني نراقب كل الولايات 👀\nكي تفتح ولايتك نبعثلك فوراً 🚨\n\nالأوامر:\n/status — حالة كل الولايات\n/batna — حالة باتنة بالتحديد\n/wilayas — قائمة كل الولايات")

    elif "/status" in text:
        send_message(chat_id, "⏳ نشوف كل الولايات، استنى شوية...")
        open_w = get_open_wilayas()
        if open_w:
            msg = "🟢 الولايات المفتوحة:\n" + "\n".join([f"✅ {w}" for w in open_w])
        else:
            msg = "🔴 كل الولايات مسكرة حالياً"
        send_message(chat_id, msg)

    elif "/batna" in text:
        if check_wilaya("باتنة"):
            send_message(chat_id, "🟢 باتنة فتحت التسجيل! سجل دروك 🚨")
        else:
            send_message(chat_id, "🔴 باتنة مزال مغلق، نبعثلك كي تفتح 👀")

    elif "/wilayas" in text:
        msg = "📋 الولايات اللي نراقبها:\n" + "\n".join(WILAYAS)
        send_message(chat_id, msg)

    elif any(w in text for w in ["مرحبا", "هلا", "سلام", "hi", "hello", "أهلا", "اهلا"]):
        send_message(chat_id, "أهلاً برو! 😄\nابعث /start باش تتسجل في التنبيهات")

    elif any(w in text for w in ["شكرا", "شكراً", "merci", "thanks"]):
        send_message(chat_id, "يسعدك برو! 🙏 كي تفتح ولايتك نبعثلك فوراً 🚨")

    elif any(w in text for w in ["واش", "كيفاش", "فين", "متى", "وقتاش"]):
        send_message(chat_id, "ما نعرفش وقتاش تفتح 😅 بصح كي تفتح نبعثلك فوراً! 🚨")

    else:
        send_message(chat_id, "برو ما فهمتكش 😄\nجرب:\n/start — تسجل\n/status — حالة الولايات\n/batna — حالة باتنة")

def listen_messages():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            if not chat_id or not text:
                continue
            if chat_id not in users:
                users.append(chat_id)
            smart_reply(text, chat_id)

def monitor():
    notified = []
    while True:
        for w in WILAYAS:
            if check_wilaya(w) and w not in notified:
                broadcast(f"🚨 {w} فتحت التسجيل! سجل دروك: https://adhahi.dz/register")
                notified.append(w)
            elif not check_wilaya(w) and w in notified:
                notified.remove(w)
        time.sleep(10)

print("Bot started - watching all wilayas...")
t1 = threading.Thread(target=listen_messages)
t2 = threading.Thread(target=monitor)
t1.start()
t2.start()
