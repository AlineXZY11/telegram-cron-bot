import os
import sqlite3
from datetime import datetime
import requests
import time
mport psycopg2
from urllib.parse import urlparse

# Ambil database URL dari Railway
DB_URL = os.getenv("DATABASE_URL")
db_info = urlparse(DB_URL)

def init_db():
    conn = psycopg2.connect(
        host=db_info.hostname,
        database=db_info.path[1:],
        user=db_info.username,
        password=db_info.password,
        port=db_info.port
    )

# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SCHEDULE = [
    "06:00", "07:48", "09:15", "09:36", "11:24",
    "13:12", "14:00", "15:00", "16:48", "18:15",
    "18:36", "20:24", "22:00", "22:12", "00:00"
]

# Database Setup
def init_db():
    conn = sqlite3.connect('notifications.db')
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

def send_notification():
    init_db()
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in SCHEDULE:
            # Kirim pesan
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            params = {"chat_id": CHAT_ID, "text": f"⏰ Notifikasi {now}"}
            requests.post(url, json=params)
            
            # Simpan ke database
            conn = sqlite3.connect('notifications.db')
            conn.execute("INSERT INTO logs (time) VALUES (?)", (now,))
            conn.commit()
            conn.close()
            
            print(f"Notifikasi terkirim: {now}")
            time.sleep(60)  # Hindari duplikat
        time.sleep(30)

if __name__ == "__main__":
    send_notification()
