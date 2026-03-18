from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, cors, socketio
from .routes.chat_routes import chat_bp
from .routes.analytics_routes import analytics_bp


def _normalize_origin(origin: str) -> str:
    return origin.strip().rstrip("/")


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    cors_origins = app.config.get("FRONTEND_ORIGIN", "*")
    if isinstance(cors_origins, str):
        if cors_origins.strip() == "*":
            cors_origins = "*"
        else:
            cors_origins = [
                _normalize_origin(origin)
                for origin in cors_origins.split(",")
                if origin.strip()
            ]
            if len(cors_origins) == 1:
                cors_origins = cors_origins[0]

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": cors_origins}})
    socketio.init_app(app, cors_allowed_origins=cors_origins)

    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")

    with app.app_context():
        from .models import user, message  # noqa: F401

        db.create_all()

    return app


__all__ = ["create_app", "socketio"]
