from flask import Blueprint, jsonify, request
from API.controllers import rota_controller as ctl

rota_bp = Blueprint("rota_bp", __name__)

@rota_bp.get("/linhas/<int:id_linha>/rota")
def rota_por_linha(id_linha: int):
    data, status = ctl.get_rota_por_linha(id_linha)
    return jsonify(data), status

@rota_bp.get("/paradas/<int:id_parada>/linhas")
def linhas_por_parada(id_parada: int):
    data, status = ctl.get_linhas_por_parada(id_parada)
    return jsonify(data), status

# Compatibilidade: /rotas?linha_id=123 -> mesma resposta de /linhas/<id>/rota
@rota_bp.get("/rotas")
def rotas_compat():
    linha_id = request.args.get("linha_id", type=int)
    if not linha_id:
        return jsonify({"error": "Parâmetro linha_id é obrigatório"}), 400
    data, status = ctl.get_rota_por_linha(linha_id)
    return jsonify(data), status
