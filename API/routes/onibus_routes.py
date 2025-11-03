from flask import Blueprint, jsonify, request
from API.controllers import onibus_controller as ctl

onibus_bp = Blueprint("onibus_bp", __name__)

@onibus_bp.get("")
def listar():
    data, status = ctl.listar(); return jsonify(data), status

@onibus_bp.get("/<int:id_>")
def obter(id_):
    data, status = ctl.obter(id_); return jsonify(data), status

@onibus_bp.post("")
def criar():
    data, status = ctl.criar(request.get_json(force=True)); return jsonify(data), status

@onibus_bp.put("/<int:id_>")
def atualizar(id_):
    data, status = ctl.atualizar(id_, request.get_json(force=True)); return jsonify(data), status

@onibus_bp.delete("/<int:id_>")
def deletar(id_):
    data, status = ctl.deletar(id_); return jsonify(data), status
