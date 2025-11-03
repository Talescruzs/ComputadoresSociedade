from pathlib import Path
import sys
# Garante que o diretório raiz do projeto esteja no sys.path
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
        "  pip install Flask flask-cors python-dotenv requests"
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

    # Filtro 'format' seguro: converte strings numéricas para float antes de formatar
    @app.template_filter("format")
    def safe_format(fmt, *args, **kwargs):
        def coerce(v):
            if isinstance(v, str):
                try:
                    return float(v)
                except Exception:
                    return v
            return v
        args2 = tuple(coerce(a) for a in args)
        kwargs2 = {k: coerce(v) for k, v in kwargs.items()}
        try:
            if kwargs2:
                return fmt % kwargs2
            if len(args2) == 1:
                return fmt % args2[0]
            return fmt % args2
        except Exception:
            # fallback simples
            return str(args[0] if args else "")

    # Expor API_BASE_URL aos templates
    @app.context_processor
    def inject_api_base():
        return {
            "API_BASE_URL": os.getenv("API_BASE_URL", "http://localhost:5000/api").rstrip("/")
        }

    from FRONT.routes.pages_routes import pages_bp
    app.register_blueprint(pages_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("FRONT_PORT", "5001")))
