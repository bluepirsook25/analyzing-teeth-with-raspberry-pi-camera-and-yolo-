"""
database.py  ──  MySQL helpers
"""

import pymysql
import config


def _get_connection():
    return pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )


def create_appointment(dentist: str, appointment_time: str) -> bool:
    """Insert one appointment row.  Returns True on success."""
    try:
        conn   = _get_connection()
        cursor = conn.cursor()
        sql    = "INSERT INTO appointments (dentist_name, appointment_time) VALUES (%s, %s)"
        cursor.execute(sql, (dentist, appointment_time))
        conn.commit()
        conn.close()
        print(f"💾 Appointment saved → {dentist} at {appointment_time}")
        return True
    except Exception as exc:
        print(f"❌ DB Error: {exc}")
        return False


def get_all_appointments() -> list:
    """Return all appointment rows as a list of dicts."""
    try:
        conn   = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments ORDER BY appointment_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as exc:
        print(f"❌ DB Error: {exc}")
        return []
