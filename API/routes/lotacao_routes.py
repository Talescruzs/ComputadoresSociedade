from flask import Blueprint, jsonify, request
from API.controllers import lotacao_controller as ctl

lotacao_bp = Blueprint("lotacao_bp", __name__)

@lotacao_bp.get("")
def listar():
    data, status = ctl.listar(); return jsonify(data), status

@lotacao_bp.get("/<int:id_>")
def obter(id_):
    data, status = ctl.obter(id_); return jsonify(data), status

@lotacao_bp.post("")
def criar():
    data, status = ctl.criar(request.get_json(force=True)); return jsonify(data), status

@lotacao_bp.put("/<int:id_>")
def atualizar(id_):
    data, status = ctl.atualizar(id_, request.get_json(force=True)); return jsonify(data), status

@lotacao_bp.delete("/<int:id_>")
def deletar(id_):
    data, status = ctl.deletar(id_); return jsonify(data), status
