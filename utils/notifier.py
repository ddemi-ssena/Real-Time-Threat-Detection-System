import os
import requests
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yükler
load_dotenv()

# Telegram bilgileri
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(photo_path, message):
    """
    Belirtilen fotoğrafı ve mesajı Telegram bot API üzerinden gönderir.
    Bu işlem ana sistemi (FPS'yi) etkilememesi için ayrı bir thread'de çağrılmalıdır.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(">>> UYARI: Telegram Bot Token veya Chat ID eksik! Bildirim gönderilemedi.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    try:
        # Fotoğrafı multipart olarak oku
        with open(photo_path, "rb") as photo:
            files = {"photo": photo}
            payload = {"chat_id": TELEGRAM_CHAT_ID, "caption": message}
            
            response = requests.post(url, data=payload, files=files, timeout=10)
            
            if response.status_code == 200:
                print(f">>> TELEGRAM BİLDİRİMİ GÖNDERİLDİ: {message}")
                return True
            else:
                print(f">>> UYARI: Telegram Error {response.status_code}: {response.text}")
                return False
    except Exception as e:
        print(f">>> HATA: Telegram bildirim gönderimi başarısız: {e}")
        return False
