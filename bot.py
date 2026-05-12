import requests
import time
from src.config import TELEGRAM_TOKEN, CHAT_ID

def attempt_registration(user_id, appointment_date):
    """
    هذه الدالة هي 'الهجوم'؛ ترسل طلب تسجيل للسيت وتتأكد إذا تم قبولك
    """
    url = "https://aid.dz/api/register"  # مثال لرابط التسجيل
    payload = {
        "user_id": user_id,
        "date": appointment_date
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 201: # إذا رجع السيت كود 201 يعني نجحت
            return True
    except Exception as e:
        print(f"Error during attack: {e}")
    
    return False

def attack_loop():
    """
    حلقة الهجوم: لا تتوقف عن المحاولة حتى يفتح السيت أو ينجح التسجيل
    """
    print("🚀 بدء الهجوم على سيت الأضاحي...")
    while True:
        if attempt_registration("123456789", "2026-06-01"):
            print("✅ تم التسجيل بنجاح! توقف عن الهجوم.")
            break
        else:
            print("❌ السيت مازال مغلق، إعادة المحاولة بعد 5 ثواني...")
            time.sleep(5)
