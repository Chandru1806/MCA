import os
from flask import Flask
from modules.ingestion import ingestion_bp

def create_app():
    app = Flask(__name__)

    # ✅ Required for flash messages in repair route
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    # 📁 Folder paths
    app.config["UPLOAD_FOLDER"] = os.path.join("storage", "uploads")
    app.config["OUTPUT_FOLDER"] = os.path.join("storage", "outputs")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    # 🔗 Register Blueprint
    app.register_blueprint(ingestion_bp)

    # 🔄 Default route
    @app.get("/")
    def home():
        return '<meta http-equiv="refresh" content="0; url=/ingestion" />'

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
