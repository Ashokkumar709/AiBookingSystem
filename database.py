import sqlite3
from datetime import datetime

conn = sqlite3.connect("bookings.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    booking_type TEXT,
    date TEXT,
    time TEXT,
    status TEXT,
    created_at TEXT
)
""")

conn.commit()

def save_booking(data):
    cur.execute(
        "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
        (data["name"], data["email"], data["phone"])
    )
    customer_id = cur.lastrowid

    cur.execute(
        """INSERT INTO bookings
        (customer_id, booking_type, date, time, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (
            customer_id,
            data["booking_type"],
            data["date"],
            data["time"],
            "confirmed",
            datetime.now().isoformat()
        )
    )
    conn.commit()
    return cur.lastrowid
