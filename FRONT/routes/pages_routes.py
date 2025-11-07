from flask import Blueprint, render_template, request, redirect, url_for
from FRONT.controllers import dashboard_controller as ctl

pages_bp = Blueprint("pages_bp", __name__)

@pages_bp.get("/")
def home():
    ctx = ctl.dashboard()
    return render_template("dashboard.html", **ctx)

@pages_bp.post("/onibus")
def criar_onibus():
    form = request.form.to_dict()
    ctl.criar_onibus(form)
    return redirect(url_for("pages_bp.home", msg="onibus_ok"))

@pages_bp.get("/insights")
def insights():
    return render_template("insights.html")

@pages_bp.get("/linhas-detalhes")
def linhas_detalhes():
    return render_template("linhas.html")

@pages_bp.get("/onibus-detalhes")
def onibus_detalhes():
    return render_template("onibus.html")

@pages_bp.get("/viagens-detalhes")
def viagens_detalhes():
    return render_template("viagens.html")

# Novo: detalhes das paradas
@pages_bp.get("/paradas-detalhes")
def paradas_detalhes():
    return render_template("paradas.html")

# Novo: detalhes específicos da parada (por id)
@pages_bp.get("/paradas-detalhes/<int:id_parada>")
def parada_detalhes(id_parada: int):
    return render_template("parada_detalhes.html")

# Novo: detalhes da viagem
@pages_bp.get("/viagens-detalhes/<int:id_viagem>")
def viagem_detalhe(id_viagem: int):
    return render_template("viagem_detalhes.html")
