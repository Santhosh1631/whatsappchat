import re
from collections import Counter

from sqlalchemy import func

from chat_importer.extensions import db
from chat_importer.models.message import Message
from chat_importer.models.user import User

STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "to",
    "in",
    "of",
    "is",
    "it",
    "for",
    "on",
    "at",
    "i",
    "you",
    "we",
    "they",
    "this",
    "that",
    "with",
}


def get_chat_analytics():
    total_messages = db.session.query(func.count(Message.id)).scalar() or 0

    most_active = (
        db.session.query(User.name, func.count(Message.id).label("count"))
        .join(Message, Message.sender_id == User.id)
        .group_by(User.id)
        .order_by(func.count(Message.id).desc())
        .first()
    )

    per_day = (
        db.session.query(func.date(Message.timestamp).label("day"), func.count(Message.id))
        .group_by(func.date(Message.timestamp))
        .order_by(func.date(Message.timestamp).asc())
        .all()
    )

    all_text = " ".join(
        row.message for row in Message.query.filter(Message.type == "text").all() if row.message
    )
    words = re.findall(r"[A-Za-z']{3,}", all_text.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    freq = Counter(filtered).most_common(20)

    return {
        "total_messages": total_messages,
        "most_active_user": {
            "name": most_active[0],
            "count": int(most_active[1]),
        }
        if most_active
        else None,
        "messages_per_day": [{"date": str(day), "count": int(count)} for day, count in per_day],
        "word_frequency": [{"word": w, "count": c} for w, c in freq],
    }
