from flask import Blueprint, jsonify, request
from API.controllers import viagem_controller as ctl

viagem_bp = Blueprint("viagem_bp", __name__)

@viagem_bp.get("")
def listar():
    data, status = ctl.listar(); return jsonify(data), status

@viagem_bp.get("/<int:id_>")
def obter(id_):
    data, status = ctl.obter(id_); return jsonify(data), status

@viagem_bp.post("")
def criar():
    data, status = ctl.criar(request.get_json(force=True)); return jsonify(data), status

@viagem_bp.put("/<int:id_>")
def atualizar(id_):
    data, status = ctl.atualizar(id_, request.get_json(force=True)); return jsonify(data), status

@viagem_bp.delete("/<int:id_>")
def deletar(id_):
    data, status = ctl.deletar(id_); return jsonify(data), status
