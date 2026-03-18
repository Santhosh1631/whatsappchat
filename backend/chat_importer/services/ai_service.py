from collections import Counter

from chat_importer.models.message import Message


POSITIVE_WORDS = {
    "great",
    "good",
    "awesome",
    "love",
    "happy",
    "nice",
    "thanks",
    "excellent",
}
NEGATIVE_WORDS = {
    "bad",
    "sad",
    "angry",
    "hate",
    "terrible",
    "worse",
    "sorry",
    "problem",
}


def generate_chat_summary(limit: int = 200):
    messages = (
        Message.query.order_by(Message.timestamp.asc()).limit(limit).all()
    )

    if not messages:
        return "No messages found to summarize."

    participants = [m.sender.name for m in messages if m.sender]
    top_people = Counter(participants).most_common(3)

    lines = []
    lines.append(f"This chat sample contains {len(messages)} messages.")

    if top_people:
        active = ", ".join([f"{name} ({count})" for name, count in top_people])
        lines.append(f"Most active participants: {active}.")

    media_count = sum(1 for m in messages if m.type == "media")
    system_count = sum(1 for m in messages if m.type == "system")
    lines.append(f"Media messages: {media_count}; system events: {system_count}.")

    first = messages[0].timestamp
    last = messages[-1].timestamp
    lines.append(f"Timeline: {first.isoformat()} to {last.isoformat()}.")

    return " ".join(lines)


def sentiment_snapshot(limit: int = 500):
    messages = (
        Message.query.filter(Message.type == "text")
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .all()
    )

    pos = 0
    neg = 0
    for m in messages:
        words = set((m.message or "").lower().split())
        pos += len(words & POSITIVE_WORDS)
        neg += len(words & NEGATIVE_WORDS)

    if pos == neg:
        label = "neutral"
    else:
        label = "positive" if pos > neg else "negative"

    return {
        "label": label,
        "positive_score": pos,
        "negative_score": neg,
        "sample_size": len(messages),
    }
