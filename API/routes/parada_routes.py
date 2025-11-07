from flask import Blueprint, jsonify, request
from API.controllers import parada_controller as ctl

parada_bp = Blueprint("parada_bp", __name__)

@parada_bp.get("")
def listar():
    data, status = ctl.listar(); return jsonify(data), status

@parada_bp.get("/<int:id_>")
def obter(id_):
    data, status = ctl.obter(id_); return jsonify(data), status

@parada_bp.post("")
def criar():
    data, status = ctl.criar(request.get_json(force=True)); return jsonify(data), status

@parada_bp.put("/<int:id_>")
def atualizar(id_):
    data, status = ctl.atualizar(id_, request.get_json(force=True)); return jsonify(data), status

@parada_bp.delete("/<int:id_>")
def deletar(id_):
    data, status = ctl.deletar(id_); return jsonify(data), status

@parada_bp.get("/pessoas-total")
def pessoas_total():
    data, status = ctl.listar_pessoas_total()
    return jsonify(data), status

# Novo: embarques por hora na parada
@parada_bp.get("/<int:id_>/pessoas-por-hora")
def pessoas_por_hora(id_):
    data, status = ctl.listar_pessoas_por_hora(id_)
    return jsonify(data), status
