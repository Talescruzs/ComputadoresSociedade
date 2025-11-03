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
    # Redireciona com flag de sucesso (usado pelo toast)
    return redirect(url_for("pages_bp.home", msg="onibus_ok"))

# Nova página de gráficos e correlações
@pages_bp.get("/insights")
def insights():
    return render_template("insights.html")
