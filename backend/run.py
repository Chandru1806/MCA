import os
import tempfile
from flask import Flask, request, send_file
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import text
from dotenv import load_dotenv

# Test: GitHub Actions Auto-Deployment

from app import db
from app.services.ingestion import ingestion_bp
from app.services.preprocessing import preprocess_csv
from app.config import Config

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='app/templates')
    
    # Enable CORS for frontend communication with explicit settings
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, 
         resources={r"/*": {"origins": cors_origins}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Accept"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         expose_headers=["Content-Type", "Authorization"],
         max_age=3600)

    # Required for flash messages in repair route
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.JWT_REFRESH_TOKEN_EXPIRES
    
    db.init_app(app)
    jwt.init_app(app)

    # Folder paths
    app.config["UPLOAD_FOLDER"] = os.path.join("storage", "uploads")
    app.config["OUTPUT_FOLDER"] = os.path.join("storage", "outputs")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    # Register Blueprints
    app.register_blueprint(ingestion_bp)
    
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    
    from app.routes.pdf_routes import pdf_bp
    app.register_blueprint(pdf_bp)
    
    from app.controllers.transaction_controller import transaction_bp
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
    
    from app.controllers.categorization_controller import categorization_bp
    app.register_blueprint(categorization_bp, url_prefix='/api/categorization')
    
    from app.controllers.dashboard_controller import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    from app.controllers.analytics_controller import analytics_bp
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
    
    from app.controllers.budget_controller import budget_bp
    app.register_blueprint(budget_bp, url_prefix='/api/budgets')
    
    from app.routes.preference_routes import preference_bp
    app.register_blueprint(preference_bp)

    # Default route
    @app.get("/")
    def home():
        return '<meta http-equiv="refresh" content="0; url=/ingestion" />'
    
    # # Database connection test
    # @app.get("/test-db")
    # def test_db():
    #     try:
    #         db.session.execute(text("SELECT 1"))
    #         return {"status": "success", "message": "Database connection successful!"}, 200
    #     except Exception as e:
    #         return {"status": "error", "message": str(e)}, 500
    
    # Your /preprocess_csv route goes inside here
    @app.route("/preprocess_csv", methods=["POST"])
    def preprocess_csv_route():
        file = request.files["csv_file"]
        if not file:
            return "No CSV uploaded", 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            file.save(tmp.name)
            repaired_path = preprocess_csv.run(tmp.name)
            return send_file(repaired_path, as_attachment=True)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
