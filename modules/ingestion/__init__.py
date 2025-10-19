from flask import Blueprint
ingestion_bp = Blueprint("ingestion", __name__)
from . import routes  # noqa: E402,F401
