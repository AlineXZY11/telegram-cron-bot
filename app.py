import os
import sqlite3
from datetime import datetime
import requests
import time

# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Ambil dari secret Fly.io
CHAT_ID = os.getenv("CHAT_ID")      # Ambil dari secret Fly.io
SCHEDULE = [
    "06:00", "07:48", "09:15", "09:36", "11:24",
    "13:12", "14:00", "15:00", "16:48", "18:15",
    "18:36", "20:24", "22:00", "22:12", "00:00"
]

# Database SQLite
def init_db():
    conn = sqlite3.connect('/data/notifications.db')  # Simpan di volume persisten
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_log(time):
    conn = sqlite3.connect('/data/notifications.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (time) VALUES (?)", (time,))
    conn.commit()
    conn.close()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=params)

def check_schedule():
    init_db()
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in SCHEDULE:
            message = f"🔔 Notifikasi {now}"
            send_telegram_message(message)
            save_log(now)
            time.sleep(60)  # Hindari duplikasi dalam 1 menit
        time.sleep(30)  # Cek setiap 30 detik

if __name__ == "__main__":
    check_schedule()
