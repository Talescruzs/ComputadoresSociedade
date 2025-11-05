from flask import Blueprint, jsonify
from API.controllers import analytics_controller as ctl

analytics_bp = Blueprint("analytics_bp", __name__)

@analytics_bp.get("/lotacao-por-linha")
def por_linha():
    data, status = ctl.lotacao_por_linha(); return jsonify(data), status

@analytics_bp.get("/lotacao-por-trecho")
def por_trecho():
    data, status = ctl.lotacao_por_trecho(); return jsonify(data), status

@analytics_bp.get("/lotacao-horaria")
def horaria():
    data, status = ctl.lotacao_horaria(); return jsonify(data), status

@analytics_bp.get("/linha/<int:id_linha>/horaria")
def horaria_linha(id_linha: int):
    data, status = ctl.lotacao_horaria_por_linha(id_linha)
    return jsonify(data), status

@analytics_bp.get("/linha/<int:id_linha>/trechos")
def trechos_linha(id_linha: int):
    data, status = ctl.trechos_por_linha(id_linha)
    return jsonify(data), status
