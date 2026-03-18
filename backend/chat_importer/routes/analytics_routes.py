from flask import Blueprint, jsonify

from chat_importer.services import get_chat_analytics

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.get("/analytics")
def get_analytics():
    return jsonify(get_chat_analytics())
