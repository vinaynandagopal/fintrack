from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    CORS(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.category_routes import category_bp
    from app.routes.transaction_routes import transaction_bp
    from app.routes.budget_routes import budget_bp
    from app.routes.savings_routes import savings_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(transaction_bp, url_prefix="/api/transactions")
    app.register_blueprint(budget_bp, url_prefix="/api/budgets")
    app.register_blueprint(savings_bp, url_prefix="/api/savings-goals")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "message": "FinTrack backend is running"}, 200

    return app