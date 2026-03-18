import re
from datetime import datetime
from typing import Dict, List, Optional


MESSAGE_PATTERNS = [
    # 12/31/23, 11:59 PM - Name: text
    re.compile(
        r"^\s*(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),?\s+(?P<time>\d{1,2}[:.]\d{2}(?::\d{2})?\s?(?:[AaPp]\.?[Mm]\.?)?)\s+[\-\u2013\u2014]\s+(?P<body>.+)$"
    ),
    # [12/31/23, 11:59 PM] Name: text
    re.compile(
        r"^\s*\[(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(?P<time>\d{1,2}[:.]\d{2}(?::\d{2})?\s?(?:[AaPp]\.?[Mm]\.?)?)\]\s*(?P<body>.+)$"
    ),
]

MEDIA_RE = re.compile(
    r"^\s*(?:<media omitted>|image omitted|video omitted|audio omitted|sticker omitted|document omitted|gif omitted|this message was deleted)\s*$",
    re.IGNORECASE,
)

MEDIA_TOKEN_RE = re.compile(r"<media omitted>", re.IGNORECASE)

SYSTEM_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"joined",
        r"left",
        r"added",
        r"removed",
        r"created group",
        r"changed (?:the )?subject",
        r"changed this group(?:'s|’) icon",
        r"messages and calls are end-to-end encrypted",
        r"security code",
    ]
]


def _normalize_time(time_str: str) -> str:
    cleaned = re.sub(r"\s+", " ", time_str.strip()).replace(".", ":")
    cleaned = cleaned.replace("a:m", "am").replace("p:m", "pm")
    cleaned = cleaned.replace("A.M.", "AM").replace("P.M.", "PM")
    return cleaned


def _match_start_of_message(line: str):
    for pattern in MESSAGE_PATTERNS:
        match = pattern.match(line)
        if match:
            return match
    return None


def _parse_datetime(date_str: str, time_str: str) -> Optional[datetime]:
    normalized_date = date_str.replace("-", "/").strip()
    normalized_time = _normalize_time(time_str)

    date_parts = normalized_date.split("/")
    if len(date_parts) != 3:
        return None

    d1, d2, year = date_parts
    if len(year) == 2:
        year = f"20{year}"

    # Heuristic: if one part > 12 that part is day, else prefer day-first.
    try:
        p1 = int(d1)
        p2 = int(d2)
    except ValueError:
        return None

    candidates = []

    if p1 > 12 and p2 <= 12:
        candidates.append(("%d/%m/%Y", f"{d1}/{d2}/{year}"))
    elif p2 > 12 and p1 <= 12:
        candidates.append(("%m/%d/%Y", f"{d1}/{d2}/{year}"))
    else:
        candidates.append(("%d/%m/%Y", f"{d1}/{d2}/{year}"))
        candidates.append(("%m/%d/%Y", f"{d1}/{d2}/{year}"))

    time_formats = ["%H:%M", "%H:%M:%S", "%I:%M %p", "%I:%M:%S %p"]

    for date_fmt, date_value in candidates:
        for t_fmt in time_formats:
            try:
                return datetime.strptime(f"{date_value} {normalized_time.upper()}", f"{date_fmt} {t_fmt}")
            except ValueError:
                continue
    return None


def _split_sender_and_message(body: str) -> Dict[str, Optional[str]]:
    # Most WhatsApp user messages follow: Sender: Message
    if ": " in body:
        sender, message = body.split(": ", 1)
        if sender and len(sender) <= 128:
            return {"sender": sender.strip(), "message": message.strip()}

    return {"sender": None, "message": body.strip()}


def _detect_type(message: str, sender: Optional[str]) -> str:
    if MEDIA_RE.match(message):
        return "media"

    if sender is None:
        for pattern in SYSTEM_PATTERNS:
            if pattern.search(message):
                return "system"
        return "system"

    return "text"


def parse_whatsapp_chat(raw_text: str) -> Dict[str, object]:
    lines = raw_text.splitlines()
    messages: List[Dict[str, object]] = []
    current: Optional[Dict[str, object]] = None
    parse_errors = 0

    def flush_current():
        if not current:
            return

        current["message"] = current["message"].strip()
        current["type"] = _detect_type(current["message"], current.get("sender"))
        messages.append(current.copy())

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        match = _match_start_of_message(line)

        if match:
            if current:
                flush_current()

            dt = _parse_datetime(match.group("date"), match.group("time"))
            split = _split_sender_and_message(match.group("body"))

            if not dt:
                parse_errors += 1
                # Keep a best-effort timestamp so records remain sortable.
                dt = datetime.utcnow()

            current = {
                "timestamp": dt,
                "sender": split["sender"],
                "message": split["message"],
                "type": "text",
            }
        else:
            if current is not None:
                if line.strip() != "":
                    current["message"] = f"{current['message']}\n{line}".strip()
            elif line.strip():
                parse_errors += 1

    if current:
        flush_current()

    media_count = 0
    system_count = 0
    for item in messages:
        if MEDIA_RE.match(item["message"]):
            item["message"] = "[Media]"
        else:
            item["message"] = MEDIA_TOKEN_RE.sub("[Media]", item["message"])

        if item["type"] == "media":
            media_count += 1
        elif item["type"] == "system":
            system_count += 1

    participants = sorted({m["sender"] for m in messages if m.get("sender")})

    return {
        "messages": sorted(messages, key=lambda x: x["timestamp"]),
        "participants": participants,
        "stats": {
            "total_messages": len(messages),
            "parse_errors": parse_errors,
            "media_messages": media_count,
            "system_messages": system_count,
        },
    }
