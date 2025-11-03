from flask import Blueprint, jsonify
from datetime import datetime

system_bp = Blueprint("system_bp", __name__)

@system_bp.get("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@system_bp.get("/")
def index():
    return jsonify({"message": "Dashboard de Transporte Público API"})
