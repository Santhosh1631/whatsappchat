from typing import Dict, List
from sqlalchemy.exc import OperationalError

from chat_importer.extensions import db
from chat_importer.models.user import User
from chat_importer.models.message import Message


def _get_or_create_users(participants: List[str]) -> Dict[str, User]:
    user_map: Dict[str, User] = {}

    for name in participants:
        existing = User.query.filter_by(name=name).first()
        if existing:
            user_map[name] = existing
            continue

        created = User(name=name)
        db.session.add(created)
        db.session.flush()
        user_map[name] = created

    return user_map


def persist_parsed_chat(parsed: Dict[str, object]) -> Dict[str, int]:
    try:
        return _persist_parsed_chat_once(parsed)
    except OperationalError:
        # Render Postgres can occasionally drop pooled SSL connections.
        # Reset the current transaction and retry once with a fresh connection.
        db.session.rollback()
        db.engine.dispose()
        return _persist_parsed_chat_once(parsed)


def _persist_parsed_chat_once(parsed: Dict[str, object]) -> Dict[str, int]:
    participants = parsed.get("participants", [])
    messages = parsed.get("messages", [])

    # One uploaded file is treated as one complete conversation thread.
    # Replace prior imported data to avoid mixing multiple histories.
    Message.query.delete()
    User.query.delete()
    db.session.flush()

    user_map = _get_or_create_users(participants)

    inserted_messages = 0
    for item in messages:
        sender_name = item.get("sender")
        sender = user_map.get(sender_name) if sender_name else None

        row = Message(
            sender_id=sender.id if sender else None,
            message=item["message"],
            timestamp=item["timestamp"],
            type=item.get("type", "text"),
            is_imported=True,
        )
        db.session.add(row)
        inserted_messages += 1

    db.session.commit()

    return {
        "users_created_or_reused": len(user_map),
        "messages_inserted": inserted_messages,
    }
