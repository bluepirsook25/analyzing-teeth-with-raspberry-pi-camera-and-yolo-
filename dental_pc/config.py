"""
config.py  ──  All settings in one place.
Values come from .env first; defaults shown below as fallback.
"""

import os
from dotenv import load_dotenv

load_dotenv()   # reads .env file if present

# ── Raspberry Pi ──────────────────────────────────────────────────────────────
PI_HOST     = os.getenv('PI_HOST',     '192.168.0.169')
PI_USER     = os.getenv('PI_USER',     'sam')
PI_PASSWORD = os.getenv('PI_PASSWORD', '1234')

# ── MySQL Database ────────────────────────────────────────────────────────────
DB_HOST     = os.getenv('DB_HOST',     'localhost')
DB_USER     = os.getenv('DB_USER',     'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME     = os.getenv('DB_NAME',     'dental_db')

# ── Flask ─────────────────────────────────────────────────────────────────────
FLASK_SECRET = os.getenv('FLASK_SECRET', 'change_me_in_production')

# ── Website login ─────────────────────────────────────────────────────────────
VALID_USER = "user"
VALID_PASS = "01011990"   # Date of birth used as password

# ── YOLO model ────────────────────────────────────────────────────────────────
MODEL_PATH  = os.path.join('models', 'yolov8n-seg.pt')

# ── File paths ────────────────────────────────────────────────────────────────
DATA_DIR        = 'data'
ORIGINAL_IMAGE  = os.path.join(DATA_DIR, 'original_teeth.jpg')
CAPTURED_IMAGE  = os.path.join(DATA_DIR, 'captured_teeth.jpg')
ANNOTATED_IMAGE = os.path.join(DATA_DIR, 'annotated_teeth.jpg')
ICS_FILE        = os.path.join(DATA_DIR, 'appointments.ics')

# ── Analysis thresholds ───────────────────────────────────────────────────────
COLOR_THRESHOLD     = 0.85   # histogram correlation — below = colour issue
STRUCTURE_THRESHOLD = 0.50   # YOLO mean confidence — below = structure issue
