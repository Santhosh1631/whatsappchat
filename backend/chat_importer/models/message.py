from chat_importer.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, default="text", index=True)
    is_imported = db.Column(db.Boolean, nullable=False, default=True)

    sender = db.relationship("User", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "sender_name": self.sender.name if self.sender else None,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            "type": self.type,
            "is_imported": self.is_imported,
        }
