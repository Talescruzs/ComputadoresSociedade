import os
from pathlib import Path
from dotenv import load_dotenv
import mysql.connector

BASE_DIR = Path(__file__).resolve().parents[1]
for env_path in (BASE_DIR / ".env", Path(__file__).resolve().parent / ".env"):
    if load_dotenv(str(env_path), override=True):
        break

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "transit_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
