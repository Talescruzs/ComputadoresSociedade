# Garantir que o diretório raiz do projeto esteja no sys.path
from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from flask import Flask
    from flask_cors import CORS
    from dotenv import load_dotenv
except ModuleNotFoundError as e:
    missing = getattr(e, "name", str(e))
    raise SystemExit(
        f"Dependência ausente: {missing}. Ative seu venv e instale com:\n"
        "  pip install Flask flask-cors python-dotenv mysql-connector-python requests"
    )
from pathlib import Path
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    base_dir = Path(__file__).resolve().parents[1]
    for env_path in (base_dir / ".env", Path(__file__).resolve().parent / ".env"):
        if load_dotenv(str(env_path), override=True):
            break

    # Registro das rotas
    from API.routes.system_routes import system_bp
    from API.routes.onibus_routes import onibus_bp
    from API.routes.linha_routes import linha_bp
    from API.routes.parada_routes import parada_bp
    from API.routes.viagem_routes import viagem_bp
    from API.routes.lotacao_routes import lotacao_bp
    from API.routes.analytics_routes import analytics_bp
    from API.routes.rota_routes import rota_bp  # <--- novo

    app.register_blueprint(system_bp)
    app.register_blueprint(onibus_bp, url_prefix="/api/onibus")
    app.register_blueprint(linha_bp, url_prefix="/api/linhas")
    app.register_blueprint(parada_bp, url_prefix="/api/paradas")
    app.register_blueprint(viagem_bp, url_prefix="/api/viagens")
    app.register_blueprint(lotacao_bp, url_prefix="/api/lotacao")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(rota_bp, url_prefix="/api")  # <--- novo
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
