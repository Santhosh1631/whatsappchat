from io import TextIOWrapper

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from chat_importer.models.message import Message
from chat_importer.models.user import User
from chat_importer.services import (
    generate_chat_summary,
    parse_whatsapp_chat,
    persist_parsed_chat,
    sentiment_snapshot,
)

chat_bp = Blueprint("chat", __name__)


@chat_bp.post("/upload-chat")
def upload_chat():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".txt"):
        return jsonify({"error": "Only .txt WhatsApp exports are supported"}), 400

    try:
        text_stream = TextIOWrapper(file.stream, encoding="utf-8", errors="replace")
        raw_text = text_stream.read()

        parsed = parse_whatsapp_chat(raw_text)
        insert_stats = persist_parsed_chat(parsed)

        return jsonify(
            {
                "message": "Chat uploaded and parsed successfully",
                "participants": parsed["participants"],
                "parse_stats": parsed["stats"],
                "insert_stats": insert_stats,
            }
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@chat_bp.get("/messages")
def get_messages():
    limit = request.args.get("limit", 500, type=int)
    offset = request.args.get("offset", 0, type=int)
    
    limit = min(limit, 5000)
    
    query = Message.query.options(joinedload(Message.sender)).order_by(Message.timestamp.asc())

    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Message.message.ilike(f"%{search}%"))

    total = query.count()
    paginated = query.limit(limit).offset(offset).all()
    return jsonify({
        "messages": [row.to_dict() for row in paginated],
        "total": total,
        "limit": limit,
        "offset": offset,
    })


@chat_bp.get("/users")
def get_users():
    rows = User.query.order_by(User.name.asc()).all()
    return jsonify([row.to_dict() for row in rows])


@chat_bp.get("/export-json")
def export_json():
    rows = Message.query.options(joinedload(Message.sender)).order_by(Message.timestamp.asc()).all()
    return jsonify({"messages": [row.to_dict() for row in rows]})


@chat_bp.get("/ai-summary")
def ai_summary():
    return jsonify({"summary": generate_chat_summary()})


@chat_bp.get("/sentiment")
def sentiment():
    return jsonify(sentiment_snapshot())
