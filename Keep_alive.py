import requests
import time

URL = "https://bossa626-crypto-bot.onrender.com"  # Thay URL nếu cần

while True:
    try:
        response = requests.get(URL)
        print(f"[{time.ctime()}] Pinged {URL}, Status: {response.status_code}")
    except Exception as e:
        print(f"[{time.ctime()}] Error: {e}")
    time.sleep(540)  # Ping mỗi 9 phút = 540 giây
