import os
import tempfile
from flask import Flask, request, send_file
from modules.ingestion import ingestion_bp
from modules.preprocessing import preprocess_csv  # Import your preprocess_csv.py module

def create_app():
    app = Flask(__name__)

    # Required for flash messages in repair route
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    # Folder paths
    app.config["UPLOAD_FOLDER"] = os.path.join("storage", "uploads")
    app.config["OUTPUT_FOLDER"] = os.path.join("storage", "outputs")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)

    # Register Blueprint
    app.register_blueprint(ingestion_bp)

    # Default route
    @app.get("/")
    def home():
        return '<meta http-equiv="refresh" content="0; url=/ingestion" />'

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
