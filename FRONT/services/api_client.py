import os
import requests

API_BASE = (os.getenv("API_BASE_URL") or "http://localhost:5000/api").rstrip("/")

def api_get(path: str):
    url = f"{API_BASE}{path}"
    try:
        r = requests.get(url, timeout=5)
        return r.json() if r.ok else None
    except Exception:
        return None

def api_post(path: str, payload: dict):
    url = f"{API_BASE}{path}"
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.json() if r.ok else None
    except Exception:
        return None
